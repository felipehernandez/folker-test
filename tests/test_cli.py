import sys

import pytest
from click.testing import CliRunner

import folker.cli
from folker.model.error import InvalidProfileSelectionException

CWD_MODULE = 'folker_cwd_import_probe'


@pytest.fixture
def isolated_import_state(monkeypatch):
    monkeypatch.setattr(sys, 'path', [p for p in sys.path if p not in ('', '.')])
    yield
    sys.modules.pop(CWD_MODULE, None)


@pytest.mark.cli
class TestWorkingDirectoryImports:
    def test_modules_in_working_directory_are_importable(self, tmp_path, monkeypatch,
                                                         isolated_import_state):
        (tmp_path / f'{CWD_MODULE}.py').write_text('def answer():\n    return 42\n')
        (tmp_path / 'test_cwd_import.yaml').write_text(
            'name: Working directory import\n'
            'stages:\n'
            '  - name: call code from working directory\n'
            '    action:\n'
            '      type: CODE\n'
            f'      module: {CWD_MODULE}\n'
            '      method: answer\n'
            '    assert:\n'
            '      - ${result} == 42\n')
        monkeypatch.chdir(tmp_path)

        result = CliRunner().invoke(folker.cli.run, ['--logger-type', 'PLAIN', '-n', '1'])

        assert result.exit_code == 0, result.output
        assert f'No module named \'{CWD_MODULE}\'' not in result.output


# @pytest.mark.cli
# class TestCli:
#     def test_empty_run(self):
#         runner = CliRunner()
#         result = runner.invoke(folker.cli.run, [])
#
#         assert result.output == ''
#
#     def test_debug_run(self):
#         runner = CliRunner()
#         result = runner.invoke(folker.cli.run, ['-d'])
#
#         assert result.output == ''
#
#     def test_trace_run(self):
#         runner = CliRunner()
#         result = runner.invoke(folker.cli.run, ['--trace'])
#
#         assert 'SETUP : start' in result.output
#         assert 'SETUP : completed' in result.output
#
#     def test_log_file_run(self, tmpdir):
#         output_file = tmpdir.join('output.txt')
#
#         runner = CliRunner()
#         result = runner.invoke(folker.cli.run, ['--trace', '-lf', str(output_file)])
#
#         assert result.output == ''
#
#         generated_logs = output_file.read()
#         assert 'SETUP : start' in generated_logs
#         assert 'SETUP : completed' in generated_logs


PASSING_TEST = ('name: Profile selection\n'
                'stages:\n'
                '  - name: print\n'
                '    action:\n'
                '      type: PRINT\n'
                '      message: hello\n')


@pytest.mark.cli
class TestProfileSelectionOnTheCommandLine:
    @pytest.fixture
    def suite(self, tmp_path, monkeypatch, isolated_import_state):
        (tmp_path / 'test_profile_selection.yaml').write_text(PASSING_TEST)
        for name in ('base', 'staging'):
            (tmp_path / f'profile_{name}.yaml').write_text(f'name: {name}\ncontext:\n  env: {name}\n')
        monkeypatch.chdir(tmp_path)

    def run(self, *args):
        return CliRunner().invoke(folker.cli.run, ['--logger-type', 'PLAIN', *args])

    def test_known_profile(self, suite):
        result = self.run('-p', 'staging', '-n', '1')

        assert result.exit_code == 0, result.output
        assert 'Stage: print' in result.output

    def test_unknown_profile_fails_before_running_any_test(self, suite):
        result = self.run('-p', 'stagin', '-n', '1')

        assert result.exit_code != 0
        assert isinstance(result.exception, InvalidProfileSelectionException)
        assert 'Stage: print' not in result.output

    def test_several_profiles_are_merged_and_the_last_one_wins(self, suite, tmp_path):
        (tmp_path / 'test_profile_selection.yaml').write_text(
            'name: Merged profiles\n'
            'stages:\n'
            '  - name: check\n'
            '    action:\n'
            '      type: PRINT\n'
            '      message: ${env} ${only_in_base}\n'
            '    assert:\n'
            '      - ${env} == "staging"\n'
            '      - ${only_in_base} == "kept"\n')
        (tmp_path / 'profile_base.yaml').write_text(
            'name: base\ncontext:\n  env: base\n  only_in_base: kept\n')

        result = self.run('-p', 'base', '-p', 'staging', '-n', '1')

        assert result.exit_code == 0, result.output

    def test_the_command_line_order_decides_the_winner(self, suite, tmp_path):
        (tmp_path / 'test_profile_selection.yaml').write_text(
            'name: Merged profiles\n'
            'stages:\n'
            '  - name: check\n'
            '    action:\n'
            '      type: PRINT\n'
            '      message: ${env}\n'
            '    assert:\n'
            '      - ${env} == "base"\n')

        result = self.run('-p', 'staging,base', '-n', '1')

        assert result.exit_code == 0, result.output

    def test_an_unknown_profile_among_several_fails(self, suite):
        result = self.run('-p', 'base', '-p', 'stagin', '-n', '1')

        assert result.exit_code != 0
        assert isinstance(result.exception, InvalidProfileSelectionException)

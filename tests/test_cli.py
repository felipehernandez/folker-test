import sys

import pytest
from click.testing import CliRunner

import folker.cli

CWD_MODULE = 'folker_cwd_import_probe'


@pytest.fixture
def isolated_import_state(monkeypatch):
    # Simulate the installed console script: the working directory is NOT on sys.path.
    monkeypatch.setattr(sys, 'path', [p for p in sys.path if p not in ('', '.')])
    yield
    sys.modules.pop(CWD_MODULE, None)


@pytest.mark.cli
class TestWorkingDirectoryImports:
    def test_modules_in_working_directory_are_importable(self, tmp_path, monkeypatch,
                                                         isolated_import_state):
        # BUG-17: protos/ and CODE modules live in the working directory, but an installed
        # `folker-test` script only has its own bin/ dir on sys.path.
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

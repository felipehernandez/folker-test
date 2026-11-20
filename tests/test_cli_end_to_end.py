"""In-process end-to-end tests of the command line (TST-05).

The Docker-free modules (print, void, wait, save, foreach, conditional, template, profile, code,
file, parallel) otherwise only run in the Docker integration jobs. Here the real `example/` fixtures
are copied into `tmp_path`, with the layout of the integration image (`test/` and `testcode/`), and
`folker.cli.run` is invoked through click with the same arguments as `docker-compose.yaml`.
Modules that need a service (REST, Postgres, Kafka, ...) stay in the Docker jobs.
"""
import shutil
import sys
from pathlib import Path

import pytest
from click.testing import CliRunner

import folker
import folker.cli
from folker.load import files
from folker.model.error import (InvalidProfileSelectionException, TestSuiteNumberExecutionsException,
                                TestSuiteResultException)

EXAMPLE = Path(__file__).resolve().parent.parent / 'example'


@pytest.fixture
def project(tmp_path, monkeypatch):
    """The integration image's layout in a temporary working directory, with a clean process state"""
    shutil.copytree(EXAMPLE / 'test', tmp_path / 'test')
    shutil.copytree(EXAMPLE / 'code', tmp_path / 'testcode')
    monkeypatch.chdir(tmp_path)

    # The run reads and fills these module-level registries and makes the working directory
    # importable: give each test its own, and forget what was imported from it
    for name in ('templates', 'stage_templates', 'profiles'):
        monkeypatch.setattr(files, name, {})
    monkeypatch.setattr(folker.executor, 'profiles', files.profiles)
    monkeypatch.setattr(sys, 'path', list(sys.path))
    yield tmp_path
    for module in [m for m in sys.modules if m == 'testcode' or m.startswith('testcode.')]:
        del sys.modules[module]


def folker_test(*arguments):
    return CliRunner().invoke(folker.cli.run, ['--logger-type', 'PLAIN', *arguments])


# The same selections and counts as the `integration-tests-*` jobs of docker-compose.yaml
DOCKER_FREE_JOBS = [
    pytest.param(['-t', 'template', '-st', 'rest', '-n', '2'], id='template'),
    pytest.param(['-p', 'test-profile', '-t', 'profile', '-n', '1'], id='profile'),
    pytest.param(['-t', 'parallel', '-n', '3'], id='parallel'),
    pytest.param(['-t', 'conditional', '-n', '1'], id='conditional'),
    pytest.param(['-t', 'foreach', '-n', '2'], id='foreach'),
    pytest.param(['-t', 'save', '-n', '2'], id='save'),
    pytest.param(['-t', 'void', '-n', '3'], id='void'),
    pytest.param(['-t', 'print', '-n', '3'], id='print'),
    pytest.param(['-t', 'wait', '-n', '1'], id='wait'),
    pytest.param(['-t', 'file', '-n', '1'], id='file'),
    pytest.param(['-t', 'code', '-n', '1'], id='code'),
]


@pytest.mark.cli
class TestDockerFreeModules:
    @pytest.mark.parametrize('arguments', DOCKER_FREE_JOBS)
    def test_the_selected_tests_pass(self, project, arguments):
        result = folker_test(*arguments)

        assert result.exception is None, result.output
        assert result.exit_code == 0, result.output

    def test_the_file_module_leaves_no_file_behind(self, project):
        folker_test('-t', 'file', '-n', '1')

        assert not (project / 'asd.txt').exists()

    def test_the_templates_are_loaded_and_used(self, project):
        result = folker_test('-t', 'template', '-st', 'rest', '-n', '2', '--debug')

        assert result.exit_code == 0, result.output
        assert 'Loaded template: simple_print_template' in result.output
        assert 'Loaded template: partial_print_template' in result.output


@pytest.mark.cli
class TestSelection:
    def test_skip_tags_remove_tests(self, project):
        # `dummy` and `void` select the void tests; skipping `conditional` drops that one
        result = folker_test('-t', 'void', '-st', 'conditional', '-n', '2')

        assert result.exit_code == 0, result.output

    def test_tags_are_combined_with_and(self, project):
        # only the conditional test is both `void` and `conditional`
        result = folker_test('-t', 'void', '-t', 'conditional', '-n', '1')

        assert result.exit_code == 0, result.output

    def test_test_files_can_be_selected_by_name(self, project):
        result = folker_test('-tf', 'test_dummy_print.yaml', '-n', '1')

        assert result.exit_code == 0, result.output

    def test_test_files_can_be_selected_by_pattern(self, project):
        result = folker_test('-TF', 'test_dummy_wait*.yaml', '-n', '1')

        assert result.exit_code == 0, result.output


@pytest.mark.cli
class TestExitStatus:
    def write_failing_test(self, project):
        (project / 'test' / 'test_failing.yaml').write_text(
            'name: Failing\n'
            'tags:\n  - failing\n'
            'stages:\n'
            '  - name: assert something false\n'
            '    action:\n'
            '      type: VOID\n'
            '    assert:\n'
            '      - 1 == 2\n')

    def test_a_failing_assertion_fails_the_run(self, project):
        self.write_failing_test(project)

        result = folker_test('-t', 'failing', '-n', '1')

        assert result.exit_code != 0
        assert isinstance(result.exception, TestSuiteResultException)
        assert result.exception.details['failure_test'] == ['Failing']

    def test_all_selected_tests_run_even_if_one_fails(self, project):
        self.write_failing_test(project)
        (project / 'test' / 'test_passing.yaml').write_text(
            'name: Passing\ntags:\n  - failing\nstages:\n  - name: ok\n    action:\n'
            '      type: VOID\n    assert:\n      - 1 == 1\n')

        result = folker_test('-t', 'failing', '-n', '2')

        assert isinstance(result.exception, TestSuiteResultException)
        assert result.exception.details['failure_test'] == ['Failing']

    def test_an_unexpected_number_of_tests_fails_the_run(self, project):
        result = folker_test('-t', 'print', '-n', '99')

        assert result.exit_code != 0
        assert isinstance(result.exception, TestSuiteNumberExecutionsException)
        assert result.exception.details == {'expected': 99, 'executed': 3}

    def test_an_unknown_profile_fails_before_any_test_runs(self, project):
        result = folker_test('-p', 'no-such-profile', '-t', 'print')

        assert result.exit_code != 0
        assert isinstance(result.exception, InvalidProfileSelectionException)
        assert 'Stage:' not in result.output


@pytest.mark.cli
class TestContextAndSecrets:
    def write(self, project):
        (project / 'test' / 'test_variables.yaml').write_text(
            'name: Variables\n'
            'tags:\n  - variables\n'
            'stages:\n'
            '  - name: check\n'
            '    action:\n'
            '      type: VOID\n'
            '    assert:\n'
            '      - ${greeting} == "hello"\n'
            '      - ${token} == "s3cr3t"\n')

    def test_variables_and_secrets_from_the_command_line(self, project):
        self.write(project)

        result = folker_test('-t', 'variables', '-n', '1',
                             '-c', 'greeting', 'hello', '-s', 'token', 's3cr3t')

        assert result.exit_code == 0, result.output

    def test_a_missing_variable_fails_the_test(self, project):
        self.write(project)

        result = folker_test('-t', 'variables', '-n', '1', '-s', 'token', 's3cr3t')

        assert isinstance(result.exception, TestSuiteResultException)

    def test_command_line_values_win_over_the_profile(self, project):
        self.write(project)
        (project / 'test' / 'profile_dev.yaml').write_text(
            'name: dev\ncontext:\n  greeting: from-profile\nsecrets:\n  token: from-profile\n')

        result = folker_test('-p', 'dev', '-t', 'variables', '-n', '1',
                             '-c', 'greeting', 'hello', '-s', 'token', 's3cr3t')

        assert result.exit_code == 0, result.output

    def test_several_profiles_are_merged_with_the_last_one_winning(self, project):
        self.write(project)
        (project / 'test' / 'profile_base.yaml').write_text(
            'name: base\ncontext:\n  greeting: base\nsecrets:\n  token: s3cr3t\n')
        (project / 'test' / 'profile_override.yaml').write_text(
            'name: override\ncontext:\n  greeting: hello\n')

        result = folker_test('-p', 'base', '-p', 'override', '-t', 'variables', '-n', '1')

        assert result.exit_code == 0, result.output

    def test_secrets_are_not_printed_by_the_trace(self, project):
        # The assertion does not contain the value, which would be printed as part of its text
        (project / 'test' / 'test_secret_length.yaml').write_text(
            'name: Secret length\n'
            'tags:\n  - secret\n'
            'stages:\n'
            '  - name: check\n'
            '    action:\n'
            '      type: VOID\n'
            '    assert:\n'
            '      - len(${token}) == 8\n')

        result = folker_test('-t', 'secret', '-n', '1', '--trace', '-s', 'token', 'xK9mQ2pL')

        assert result.exit_code == 0, result.output
        assert 'xK9mQ2pL' not in result.output
        assert '********' in result.output

from unittest.mock import patch

import pytest

from folker.parameters import parameterised, Configuration


@parameterised
def load_command_arguments(config: Configuration):
    return config


@pytest.mark.cli
class TestDebugParameter:
    @patch('sys.argv', ['method', ])
    def test_no_flag(self):
        config: Configuration = load_command_arguments(standalone_mode=False)

        assert not config.debug_mode

    @patch('sys.argv', ['method', '-d', ])
    def test_flag(self):
        config: Configuration = load_command_arguments(standalone_mode=False)

        assert config.debug_mode

    @patch('sys.argv', ['method', '--debug', ])
    def test_long_flag(self):
        config: Configuration = load_command_arguments(standalone_mode=False)

        assert config.debug_mode


@pytest.mark.cli
class TestTraceParameter:
    @patch('sys.argv', ['method', ])
    def test_no_flag(self):
        config: Configuration = load_command_arguments(standalone_mode=False)

        assert not config.trace_mode

    @patch('sys.argv', ['method', '--trace', ])
    def test_long_flag(self):
        config: Configuration = load_command_arguments(standalone_mode=False)

        assert config.trace_mode


@pytest.mark.cli
class TestLogFileParameter:
    @patch('sys.argv', ['method', ])
    def test_no_flag(self):
        config: Configuration = load_command_arguments(standalone_mode=False)

        assert config.log_file is None

    @patch('sys.argv', ['method', '-lf', 'file.txt', ])
    def test_flag(self):
        config: Configuration = load_command_arguments(standalone_mode=False)

        assert config.log_file == 'file.txt'

    @patch('sys.argv', ['method', '--log-file=file.txt', ])
    def test_long_flag(self):
        config: Configuration = load_command_arguments(standalone_mode=False)

        assert config.log_file == 'file.txt'


@pytest.mark.cli
class TestLoggetTypeParameter:
    @patch('sys.argv', ['method', ])
    def test_no_flag(self):
        config: Configuration = load_command_arguments(standalone_mode=False)

        assert config.logger_type is Configuration.LoggerType.COLOR

    @patch('sys.argv', ['method', '--logger-type=plain', ])
    def test_plain_flag(self):
        config: Configuration = load_command_arguments(standalone_mode=False)

        assert config.logger_type is Configuration.LoggerType.PLAIN

    @patch('sys.argv', ['method', '--logger-type=color', ])
    def test_color_flag(self):
        config: Configuration = load_command_arguments(standalone_mode=False)

        assert config.logger_type is Configuration.LoggerType.COLOR


@pytest.mark.cli
class TestTagParameter:
    @patch('sys.argv', ['method', ])
    def test_no_flag(self):
        config: Configuration = load_command_arguments(standalone_mode=False)

        assert config.execute_tags == set()

    @patch('sys.argv', ['method', '-t', 'a_tag', ])
    def test_one_tag_flag(self):
        config: Configuration = load_command_arguments(standalone_mode=False)

        assert config.execute_tags == {'a_tag'}

    @patch('sys.argv', ['method', '-t', 'a_tag', '-t', 'another_tag', ])
    def test_multiple_tag_flags(self):
        config: Configuration = load_command_arguments(standalone_mode=False)

        assert config.execute_tags == {'a_tag', 'another_tag'}

    @patch('sys.argv', ['method', '-t', 'a_tag,another_tag', ])
    def test_multiple_tags_flag(self):
        config: Configuration = load_command_arguments(standalone_mode=False)

        assert config.execute_tags == {'a_tag', 'another_tag'}

    @patch('sys.argv', ['method', '--tag=a_tag', ])
    def test_one_tag_long_flag(self):
        config: Configuration = load_command_arguments(standalone_mode=False)

        assert config.execute_tags == {'a_tag'}

    @patch('sys.argv', ['method', '--tag=a_tag', '--tag=another_tag', ])
    def test_multiple_tag_long_flags(self):
        config: Configuration = load_command_arguments(standalone_mode=False)

        assert config.execute_tags == {'a_tag', 'another_tag'}

    @patch('sys.argv', ['method', '--tag=a_tag,another_tag', ])
    def test_multiple_tags_long_flag(self):
        config: Configuration = load_command_arguments(standalone_mode=False)

        assert config.execute_tags == {'a_tag', 'another_tag'}


@pytest.mark.cli
class TestProfileParameter:
    @patch('sys.argv', ['method', ])
    def test_no_flag(self):
        config: Configuration = load_command_arguments(standalone_mode=False)

        assert config.profiles == set()

    @patch('sys.argv', ['method', '-p', 'a_profile', ])
    def test_one_profile_flag(self):
        config: Configuration = load_command_arguments(standalone_mode=False)

        assert config.profiles == {'a_profile'}

    @patch('sys.argv', ['method', '-p', 'a_profile', '-p', 'another_profile', ])
    def test_multiple_profile_flags(self):
        config: Configuration = load_command_arguments(standalone_mode=False)

        assert config.profiles == {'a_profile', 'another_profile'}

    @patch('sys.argv', ['method', '-p', 'a_profile,another_profile', ])
    def test_multiple_profiles_flag(self):
        config: Configuration = load_command_arguments(standalone_mode=False)

        assert config.profiles == {'a_profile', 'another_profile'}

    @patch('sys.argv', ['method', '--profile=a_profile', ])
    def test_one_profile_long_flag(self):
        config: Configuration = load_command_arguments(standalone_mode=False)

        assert config.profiles == {'a_profile'}

    @patch('sys.argv', ['method', '--profile=a_profile', '--profile=another_profile', ])
    def test_multiple_profile_long_flags(self):
        config: Configuration = load_command_arguments(standalone_mode=False)

        assert config.profiles == {'a_profile', 'another_profile'}

    @patch('sys.argv', ['method', '--profile=a_profile,another_profile', ])
    def test_multiple_profiles_long_flag(self):
        config: Configuration = load_command_arguments(standalone_mode=False)

        assert config.profiles == {'a_profile', 'another_profile'}


@pytest.mark.cli
class TestContextParameter:
    @patch('sys.argv', ['method', ])
    def test_no_value(self):
        config: Configuration = load_command_arguments(standalone_mode=False)

        assert config.context == {}

    @patch('sys.argv', ['method', '-c', 'key', 'value', ])
    def test_one_value(self):
        config: Configuration = load_command_arguments(standalone_mode=False)

        assert config.context == {'key': 'value'}

    @patch('sys.argv', ['method', '--context', 'key', 'value'])
    def test_one_value_long_flag(self):
        config: Configuration = load_command_arguments(standalone_mode=False)

        assert config.context == {'key': 'value'}

    @patch('sys.argv', ['method', '-c', 'key', 'value', '-c', 'key2', 'value2'])
    def test_multiple_flags(self):
        config: Configuration = load_command_arguments(standalone_mode=False)

        assert config.context == {'key': 'value', 'key2': 'value2'}


@pytest.mark.cli
class TestSecretParameter:
    @patch('sys.argv', ['method', ])
    def test_no_value(self):
        config: Configuration = load_command_arguments(standalone_mode=False)

        assert config.secrets == {}

    @patch('sys.argv', ['method', '-s', 'key', 'value', ])
    def test_one_value(self):
        config: Configuration = load_command_arguments(standalone_mode=False)

        assert config.secrets == {'key': 'value'}

    @patch('sys.argv', ['method', '--secret', 'key', 'value'])
    def test_one_value_long_flag(self):
        config: Configuration = load_command_arguments(standalone_mode=False)

        assert config.secrets == {'key': 'value'}

    @patch('sys.argv', ['method', '-s', 'key', 'value', '-s', 'key2', 'value2'])
    def test_multiple_flags(self):
        config: Configuration = load_command_arguments(standalone_mode=False)

        assert config.secrets == {'key': 'value', 'key2': 'value2'}


@pytest.mark.cli
class TestExpectedTestCountParameter:
    @patch('sys.argv', ['method', ])
    def test_no_value(self):
        config: Configuration = load_command_arguments(standalone_mode=False)

        assert config.expected_test_count is None

    @patch('sys.argv', ['method', '-n', '2'])
    def test_value(self):
        config: Configuration = load_command_arguments(standalone_mode=False)

        assert config.expected_test_count == 2


@pytest.mark.cli
class TestTestFilesParameter:
    @patch('sys.argv', ['method'])
    def test_no_value(self):
        config: Configuration = load_command_arguments(standalone_mode=False)

        assert config.test_files == set()

    @patch('sys.argv', ['method', '-tf', 'file.yaml'])
    def test_flag_simple_single(self):
        config: Configuration = load_command_arguments(standalone_mode=False)

        assert config.test_files == {'file.yaml'}

    @patch('sys.argv', ['method', '-tf', 'file1.yaml', '-tf', 'file2.yaml', ])
    def test_flag_multiple_single(self):
        config: Configuration = load_command_arguments(standalone_mode=False)

        assert config.test_files == {'file1.yaml', 'file2.yaml'}

    @patch('sys.argv', ['method', '--test-file', 'file1.yaml', ])
    def test_flag_long_simple_single(self):
        config: Configuration = load_command_arguments(standalone_mode=False)

        assert config.test_files == {'file1.yaml'}

    @patch('sys.argv', ['method', '--test-file=file1.yaml', ])
    def test_flag_long_simple_equals(self):
        config: Configuration = load_command_arguments(standalone_mode=False)

        assert config.test_files == {'file1.yaml'}

    @patch('sys.argv', ['method', '--test-file', 'file1.yaml', '--test-file', 'file2.yaml', ])
    def test_flag_long_multiple_single(self):
        config: Configuration = load_command_arguments(standalone_mode=False)

        assert config.test_files == {'file1.yaml', 'file2.yaml'}


@pytest.mark.cli
class TestTestFilesReParameter:
    @patch('sys.argv', ['method', ])
    def test_no_value(self):
        config: Configuration = load_command_arguments(standalone_mode=False)

        assert config.test_files_re == '**/test*.yaml'

    @patch('sys.argv', ['method', '-TF', 'testing*.yaml'])
    def test_flag(self):
        config: Configuration = load_command_arguments(standalone_mode=False)

        assert config.test_files_re == '**/testing*.yaml'

    @patch('sys.argv', ['method', '--TEST-FILES', 'testing*.yaml'])
    def test_long_flag(self):
        config: Configuration = load_command_arguments(standalone_mode=False)

        assert config.test_files_re == '**/testing*.yaml'

    @patch('sys.argv', ['method', '--TEST-FILES=testing*.yaml'])
    def test_long_flag_equals(self):
        config: Configuration = load_command_arguments(standalone_mode=False)

        assert config.test_files_re == '**/testing*.yaml'


@pytest.mark.cli
class TestTemplateFilesReParameter:
    @patch('sys.argv', ['method', ])
    def test_no_value(self):
        config: Configuration = load_command_arguments(standalone_mode=False)

        assert config.template_files_re == '**/template*.yaml'


@pytest.mark.cli
class TestProfileFilesReParameter:
    @patch('sys.argv', ['method', ])
    def test_no_value(self):
        config: Configuration = load_command_arguments(standalone_mode=False)

        assert config.profile_files_re == '**/profile*.yaml'

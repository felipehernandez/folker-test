from unittest.mock import patch

import pytest

from folker import is_debug, is_trace
from folker.parameters.parameters import command_options, \
    capture_parameters_context, \
    parameterised_tags, \
    parameterised_test_files, \
    test_file_regular_expression, \
    parameterised_profile, \
    parameterised, capture_parameters_secrets


@parameterised
def load_command_arguments(*args, **kargs):
    return 0


class TestStringMethods:

    @pytest.fixture(autouse=True)
    def setup(self):
        command_options.clear()
        yield

    @patch('sys.argv', ['method', '-d'])
    def test_debug_flag(self):
        load_command_arguments(standalone_mode=False)

        assert is_debug()

    @patch('sys.argv', ['method', '--debug'])
    def test_debug_flag_long(self):
        load_command_arguments(standalone_mode=False)

        assert is_debug()

    @patch('sys.argv', ['method'])
    def test_no_debug_flag(self):
        load_command_arguments(standalone_mode=False)

        assert not is_debug()

    @patch('sys.argv', ['method', '--trace'])
    def test_trace_flag_long(self):
        load_command_arguments(standalone_mode=False)

        assert is_trace()

    @patch('sys.argv', ['method'])
    def test_no_trace_flag(self):
        load_command_arguments(standalone_mode=False)

        assert not is_trace()

    @patch('sys.argv', ['method'])
    def test_capture_parameters_context_no_values(self):
        load_command_arguments(standalone_mode=False)

        assert {} == capture_parameters_context()

    @patch('sys.argv', ['method', '-c', 'key', 'value'])
    def test_capture_parameters_context_one_value(self):
        load_command_arguments(standalone_mode=False)

        assert {'key': 'value'} == capture_parameters_context()

    @patch('sys.argv', ['method', '--context', 'key', 'value'])
    def test_capture_parameters_context_long_one_value(self):
        load_command_arguments(standalone_mode=False)

        assert {'key': 'value'} == capture_parameters_context()

    @patch('sys.argv', ['method', '-c', 'key', 'value', '-c', 'key2', 'value2'])
    def test_capture_parameters_context_multiple_values(self):
        load_command_arguments(standalone_mode=False)

        assert {'key': 'value', 'key2': 'value2'} == capture_parameters_context()

    @patch('sys.argv', ['method'])
    def test_capture_parameters_secrets_no_values(self):
        load_command_arguments(standalone_mode=False)

        assert {} == capture_parameters_secrets()

    @patch('sys.argv', ['method', '-s', 'key', 'value'])
    def test_capture_parameters_secrets_one_value(self):
        load_command_arguments(standalone_mode=False)

        assert {'key': 'value'} == capture_parameters_secrets()

    @patch('sys.argv', ['method', '--secret', 'key', 'value'])
    def test_capture_parameters_secrets_long_one_value(self):
        load_command_arguments(standalone_mode=False)

        assert {'key': 'value'} == capture_parameters_secrets()

    @patch('sys.argv', ['method', '-s', 'key', 'value', '-s', 'key2', 'value2'])
    def test_capture_parameters_secrets_multiple_values(self):
        load_command_arguments(standalone_mode=False)

        assert {'key': 'value', 'key2': 'value2'} == capture_parameters_secrets()

    @patch('sys.argv', ['method', '-t', 'asd'])
    def test_tag_flag_simple_single(self):
        load_command_arguments(standalone_mode=False)

        assert ['asd'] == parameterised_tags()

    @patch('sys.argv', ['method', '-t', 'asd,asd2'])
    def test_tag_flag_simple_multiple(self):
        load_command_arguments(standalone_mode=False)

        assert ['asd', 'asd2'] == parameterised_tags()

    @patch('sys.argv', ['method', '-t', 'asd,asd2', '-t', 'asd3'])
    def test_tag_flag_simple_multiple2(self):
        load_command_arguments(standalone_mode=False)

        assert ['asd', 'asd2', 'asd3'] == parameterised_tags()

    @patch('sys.argv', ['method', '-t', 'asd', '-t', 'asd2'])
    def test_tag_flag_multiple_single(self):
        load_command_arguments(standalone_mode=False)

        assert ['asd', 'asd2'] == parameterised_tags()

    @patch('sys.argv', ['method', '-t', 'asd', '-tasd2'])
    def test_tag_flag_single_multiple(self):
        load_command_arguments(standalone_mode=False)

        assert ['asd', 'asd2'] == parameterised_tags()

    @patch('sys.argv', ['method'])
    def test_tag_flag_single_multiple(self):
        load_command_arguments(standalone_mode=False)

        assert [] == parameterised_tags()

    @patch('sys.argv', ['method', '--tag', 'asd'])
    def test_tag_flag_long_simple_single(self):
        load_command_arguments(standalone_mode=False)

        assert ['asd'] == parameterised_tags()

    @patch('sys.argv', ['method', '--tag', 'asd', '--tag', 'asd2'])
    def test_tag_flag_long_multiple_single(self):
        load_command_arguments(standalone_mode=False)

        assert ['asd', 'asd2'] == parameterised_tags()

    @patch('sys.argv', ['method', '--tag', 'asd', '--tag', 'asd2'])
    def test_tag_flag_long_single_multiple(self):
        load_command_arguments(standalone_mode=False)

        assert ['asd', 'asd2'] == parameterised_tags()

    @patch('sys.argv', ['method', '-f', 'asd'])
    def test_files_flag_simple_single(self):
        load_command_arguments(standalone_mode=False)

        assert ['asd'] == parameterised_test_files()

    @patch('sys.argv', ['method', '-f', 'asd', '-f', 'asd2'])
    def test_files_flag_multiple_single(self):
        load_command_arguments(standalone_mode=False)

        assert ['asd', 'asd2'] == parameterised_test_files()

    @patch('sys.argv', ['method'])
    def test_files_flag_single_multiple(self):
        load_command_arguments(standalone_mode=False)

        assert [] == parameterised_test_files()

    @patch('sys.argv', ['method', '--file', 'asd'])
    def test_files_flag_long_simple_single(self):
        load_command_arguments(standalone_mode=False)

        assert ['asd'] == parameterised_test_files()

    @patch('sys.argv', ['method', '--file', 'asd', '--file', 'asd2'])
    def test_files_flag_long_multiple_single(self):
        load_command_arguments(standalone_mode=False)

        assert ['asd', 'asd2'] == parameterised_test_files()

    @patch('sys.argv', ['method', '-F', 'asd'])
    def test_files_re_flag_simple_single(self):
        load_command_arguments(standalone_mode=False)

        assert '**/asd' == test_file_regular_expression()

    @patch('sys.argv', ['method', '-F', 'asd'])
    def test_files_re_flag_single_multiple(self):
        load_command_arguments(standalone_mode=False)

        assert ['asd', 'asd2'] == test_file_regular_expression()

    @patch('sys.argv', ['method'])
    def test_files_re_flag_single_multiple(self):
        load_command_arguments(standalone_mode=False)

        assert '**/test*.yaml' == test_file_regular_expression()

    @patch('sys.argv', ['method', '--FILE', 'asd'])
    def test_files_re_flag_long_simple_single(self):
        load_command_arguments(standalone_mode=False)

        assert '**/asd' == test_file_regular_expression()

    @patch('sys.argv', ['method', '-p', 'a_profile'])
    def test_profile_flag(self):
        load_command_arguments(standalone_mode=False)

        assert 'a_profile' == parameterised_profile()

    @patch('sys.argv', ['method', '--profile', 'a_profile'])
    def test_profile_flag_long(self):
        load_command_arguments(standalone_mode=False)

        assert 'a_profile' == parameterised_profile()

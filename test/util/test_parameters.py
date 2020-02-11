from unittest import TestCase
from unittest.mock import patch

from folker import is_debug, is_trace
from folker.util.parameters import command_options, capture_parameters_context, load_command_arguments


class TestStringMethods(TestCase):

    def setUp(self) -> None:
        command_options.clear()

    @patch('sys.argv', ['method', '-d'])
    def test_debug_flag(self):
        load_command_arguments()

        self.assertTrue(is_debug())

    @patch('sys.argv', ['method', '--debug'])
    def test_debug_flag_long(self):
        load_command_arguments()

        self.assertTrue(is_debug())

    @patch('sys.argv', ['method'])
    def test_no_debug_flag(self):
        load_command_arguments()

        self.assertFalse(is_debug())

    @patch('sys.argv', ['method', '-t'])
    def test_trace_flag(self):
        load_command_arguments()

        self.assertTrue(is_trace())

    @patch('sys.argv', ['method', '--trace'])
    def test_trace_flag_long(self):
        load_command_arguments()

        self.assertTrue(is_trace())

    @patch('sys.argv', ['method'])
    def test_no_trace_flag(self):
        load_command_arguments()

        self.assertFalse(is_trace())

    @patch('sys.argv', ['method'])
    def test_capture_parameters_context_no_values(self):
        load_command_arguments()

        self.assertEqual({}, capture_parameters_context())

    @patch('sys.argv', ['method', '-ckey:value'])
    def test_capture_parameters_context_one_value(self):
        load_command_arguments()

        self.assertEqual({'key': 'value'}, capture_parameters_context())

    @patch('sys.argv', ['method', '--context=key:value'])
    def test_capture_parameters_context_long_one_value(self):
        load_command_arguments()

        self.assertEqual({'key': 'value'}, capture_parameters_context())

    @patch('sys.argv', ['method', '-ckey:value', '-ckey2:value2'])
    def test_capture_parameters_context_multiple_values(self):
        load_command_arguments()

        self.assertEqual({'key': 'value', 'key2': 'value2'}, capture_parameters_context())

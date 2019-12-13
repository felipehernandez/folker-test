from unittest import TestCase
from unittest.mock import patch

from folker import is_debug, is_trace
from folker.util.parameters import capture_parameters_context


class TestStringMethods(TestCase):

    @patch('sys.argv', ['method', 'debug'])
    def test_debug_flag(self):
        self.assertTrue(is_debug())

    @patch('sys.argv', ['method'])
    def test_no_debug_flag(self):
        self.assertFalse(is_debug())

    @patch('sys.argv', ['method', 'trace'])
    def test_trace_flag(self):
        self.assertTrue(is_trace())

    @patch('sys.argv', ['method'])
    def test_no_trace_flag(self):
        self.assertFalse(is_trace())

    @patch('sys.argv', ['method'])
    def test_capture_parameters_context_no_values(self):
        self.assertEquals({}, capture_parameters_context())

    @patch('sys.argv', ['method', '-ckey=value'])
    def test_capture_parameters_context_one_value(self):
        self.assertEquals({'key': 'value'}, capture_parameters_context())

    @patch('sys.argv', ['method', '-ckey=value', '-ckey2=value2'])
    def test_capture_parameters_context_multiple_values(self):
        self.assertEquals({'key': 'value', 'key2': 'value2'}, capture_parameters_context())

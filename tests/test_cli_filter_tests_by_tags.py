from unittest.mock import Mock

from folker.cli import filter_tests_by_tags
from folker.model import Test
from folker.parameters import Configuration


class TestFilterTestByTags:
    def test_no_execute_tags_no_skip_tags_no_tagged_test(self):
        test_1 = Test(tags=[])

        filtered_tests = filter_tests_by_tags(system_logger=Mock(),
                                              config=Configuration(),
                                              tests=[test_1])

        assert filtered_tests == [test_1]

    def test_no_execute_tags_no_skip_tags_tagged_test(self):
        test_1 = Test(tags=['asd'])

        filtered_tests = filter_tests_by_tags(system_logger=Mock(),
                                              config=Configuration(),
                                              tests=[test_1])

        assert filtered_tests == [test_1]

    def test_execute_tags_no_skip_tags_no_tagged_test(self):
        test_1 = Test()

        filtered_tests = filter_tests_by_tags(system_logger=Mock(),
                                              config=Configuration(tags=['asd']),
                                              tests=[test_1])

        assert filtered_tests == []

    def test_execute_tags_no_skip_tags_tagged_test(self):
        test_1 = Test(tags=['asd'])

        filtered_tests = filter_tests_by_tags(system_logger=Mock(),
                                              config=Configuration(tags=['asd']),
                                              tests=[test_1])

        assert filtered_tests == [test_1]

    def test_execute_tags_no_skip_tags_tagged_other_test(self):
        test_1 = Test(tags=['asd2'])

        filtered_tests = filter_tests_by_tags(system_logger=Mock(),
                                              config=Configuration(tags=['asd']),
                                              tests=[test_1])

        assert filtered_tests == []

    def test_execute_multiple_tags_no_skip_tags_tagged_test(self):
        test_1 = Test(tags=['asd'])

        filtered_tests = filter_tests_by_tags(system_logger=Mock(),
                                              config=Configuration(tags=['asd', 'asd2']),
                                              tests=[test_1])

        assert filtered_tests == [test_1]

    def test_no_execute_tags_skip_tags_no_tagged_test(self):
        test_1 = Test()

        filtered_tests = filter_tests_by_tags(system_logger=Mock(),
                                              config=Configuration(skip_tags=['asd']),
                                              tests=[test_1])

        assert filtered_tests == [test_1]

    def test_no_execute_tags_skip_tags_tagged_test(self):
        test_1 = Test(tags=['asd'])

        filtered_tests = filter_tests_by_tags(system_logger=Mock(),
                                              config=Configuration(skip_tags=['asd']),
                                              tests=[test_1])

        assert filtered_tests == []

    def test_no_execute_tags_skip_tags_tagged_other_test(self):
        test_1 = Test(tags=['asd2'])

        filtered_tests = filter_tests_by_tags(system_logger=Mock(),
                                              config=Configuration(skip_tags=['asd']),
                                              tests=[test_1])

        assert filtered_tests == [test_1]

    def test_no_execute_multiple_tags_skip_tags_tagged_test(self):
        test_1 = Test(tags=['asd'])

        filtered_tests = filter_tests_by_tags(system_logger=Mock(),
                                              config=Configuration(skip_tags=['asd', 'asd2']),
                                              tests=[test_1])

        assert filtered_tests == []

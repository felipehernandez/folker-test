from unittest.mock import Mock

from folker.cli import filter_tests_by_tags
from folker.model import Test
from folker.parameters import Configuration


class TestFilterTestByTags:
    def test_no_tags_no_filtering(self, plain_console_system_logger_on_trace):
        """
        GIVEN: config: no execute tags
        GIVEN: config: no skip tags
        GIVEN: test: no tags
        WHEN: filter
        THEN: test filtered in
        """

        test_name = 'test_name'
        test_1 = Test(name=test_name, tags=[])

        filtered_tests = filter_tests_by_tags(system_logger=plain_console_system_logger_on_trace,
                                              config=Configuration(),
                                              tests=[test_1])

        assert filtered_tests == [test_1]

    def test_no_tags_no_filtering_output(self,
                                         capsys,
                                         plain_console_system_logger_on_trace):
        """
        GIVEN: config: no execute tags
        GIVEN: config: no skip tags
        GIVEN: test: no tags
        WHEN: filter
        THEN: log output = EXECUTE test
        """

        test_name = 'test_name'
        test_1 = Test(name=test_name, tags=[])

        filter_tests_by_tags(system_logger=plain_console_system_logger_on_trace,
                             config=Configuration(),
                             tests=[test_1])

        captured = capsys.readouterr()
        assert captured.out == '-' * 100 + '\n' \
               + 'Test files : filtering' + '\n' \
               + f'\t{test_name} <EXECUTE> - No skip tag matching' + '\n'

    def test_tags_no_filtering(self, plain_console_system_logger_on_trace):
        """
        GIVEN: config: no execute tags
        GIVEN: config: no skip tags
        GIVEN: test: tag
        WHEN: filter
        THEN: test filtered in
        """

        test_name = 'test_name'
        test_1 = Test(name=test_name, tags=['asd'])

        filtered_tests = filter_tests_by_tags(system_logger=plain_console_system_logger_on_trace,
                                              config=Configuration(),
                                              tests=[test_1])

        assert filtered_tests == [test_1]

    def test_tags_no_filtering_output(self,
                                      capsys,
                                      plain_console_system_logger_on_trace):
        """
        GIVEN: config: no execute tags
        GIVEN: config: no skip tags
        GIVEN: test: tag
        WHEN: filter
        THEN: log output = EXECUTE test
        """

        test_name = 'test_name'
        test_1 = Test(name=test_name, tags=['asd'])

        filter_tests_by_tags(system_logger=plain_console_system_logger_on_trace,
                             config=Configuration(),
                             tests=[test_1])

        captured = capsys.readouterr()
        assert captured.out == '-' * 100 + '\n' \
               + 'Test files : filtering' + '\n' \
               + f'\t{test_name} <EXECUTE> - No skip tag matching' + '\n'

    def test_no_tag_test_not_matching_execution_tags(self, plain_console_system_logger_on_trace):
        """
        GIVEN: config: execute tag
        GIVEN: config: no skip tags
        GIVEN: test: no tags
        WHEN: filter
        THEN: test filtered out
        """

        test_name = 'test_name'
        test_1 = Test(name=test_name, tags=[])

        filtered_tests = filter_tests_by_tags(system_logger=plain_console_system_logger_on_trace,
                                              config=Configuration(tags=['asd']),
                                              tests=[test_1])

        assert filtered_tests == []

    def test_no_tag_test_not_matching_execution_tags_output(self,
                                                            capsys,
                                                            plain_console_system_logger_on_trace):
        """
        GIVEN: config: execute tag
        GIVEN: config: no skip tags
        GIVEN: test: no tags
        WHEN: filter
        THEN: log output = SKIP
        """

        test_name = 'test_name'
        test_1 = Test(name=test_name, tags=[])

        filter_tests_by_tags(system_logger=plain_console_system_logger_on_trace,
                             config=Configuration(tags=['asd']),
                             tests=[test_1])

        captured = capsys.readouterr()
        assert captured.out == '-' * 100 + '\n' \
               + 'Test files : filtering' + '\n' \
               + f'\t{test_name} <SKIP> - No execute tag matching' + '\n'

    def test_tagged_test_matching_execution_tags(self, plain_console_system_logger_on_trace):
        """
        GIVEN: config: execute tag
        GIVEN: config: no skip tags
        GIVEN: test: matching tag
        WHEN: filter
        THEN: test filtered in
        """

        test_name = 'test_name'
        test_1 = Test(name=test_name, tags=['asd'])

        filtered_tests = filter_tests_by_tags(system_logger=Mock(),
                                              config=Configuration(tags=['asd']),
                                              tests=[test_1])

        assert filtered_tests == [test_1]

    def test_tagged_test_matching_execution_tags_output(self,
                                                        capsys,
                                                        plain_console_system_logger_on_trace):
        """
        GIVEN: config: execute tag
        GIVEN: config: no skip tags
        GIVEN: test: matching tag
        WHEN: filter
        THEN: log output = EXECUTE
        """

        test_name = 'test_name'
        test_1 = Test(name=test_name, tags=['asd'])

        filter_tests_by_tags(system_logger=plain_console_system_logger_on_trace,
                             config=Configuration(tags=['asd']),
                             tests=[test_1])

        captured = capsys.readouterr()
        assert captured.out == '-' * 100 + '\n' \
               + 'Test files : filtering' + '\n' \
               + f"\t{test_name} <EXECUTE> - Execute tag matching : {{'asd'}}" + '\n'

    def test_tagged_test_not_matching_execution_tags(self, plain_console_system_logger_on_trace):
        """
        GIVEN: config: execute tag
        GIVEN: config: no skip tags
        GIVEN: test: not matching tag
        WHEN: filter
        THEN: test filtered out
        """

        test_name = 'test_name'
        test_1 = Test(name=test_name, tags=['asd2'])

        filtered_tests = filter_tests_by_tags(system_logger=plain_console_system_logger_on_trace,
                                              config=Configuration(tags=['asd']),
                                              tests=[test_1])

        assert filtered_tests == []

    def test_tagged_test_not_matching_execution_tags_output(self,
                                                            capsys,
                                                            plain_console_system_logger_on_trace):
        """
        GIVEN: config: execute tag
        GIVEN: config: no skip tags
        GIVEN: test: not matching tag
        WHEN: filter
        THEN: log output = SKIP
        """

        test_name = 'test_name'
        test_1 = Test(name=test_name, tags=['asd2'])

        filter_tests_by_tags(system_logger=plain_console_system_logger_on_trace,
                             config=Configuration(tags=['asd']),
                             tests=[test_1])

        captured = capsys.readouterr()
        assert captured.out == '-' * 100 + '\n' \
               + 'Test files : filtering' + '\n' \
               + f'\t{test_name} <SKIP> - No execute tag matching' + '\n'

    def test_one_execution_tag_matching(self, plain_console_system_logger_on_trace):
        """
        GIVEN: config: execute tags
        GIVEN: config: no skip tags
        GIVEN: test: matching tags
        WHEN: filter
        THEN: test filtered in
        """

        test_1 = Test(tags=['asd'])

        filtered_tests = filter_tests_by_tags(system_logger=plain_console_system_logger_on_trace,
                                              config=Configuration(tags=['asd', 'asd2']),
                                              tests=[test_1])

        assert filtered_tests == [test_1]

    def test_one_execution_tag_matching_output(self,
                                               capsys,
                                               plain_console_system_logger_on_trace):
        """
        GIVEN: config: execute tags
        GIVEN: config: no skip tags
        GIVEN: test: matching tags
        WHEN: filter
        THEN: log output = EXECUTE test
        """

        test_name = 'test_name'
        test_1 = Test(name=test_name, tags=['asd'])

        filter_tests_by_tags(system_logger=plain_console_system_logger_on_trace,
                             config=Configuration(tags=['asd', 'asd2']),
                             tests=[test_1])

        captured = capsys.readouterr()
        assert captured.out == '-' * 100 + '\n' \
               + 'Test files : filtering' + '\n' \
               + f"\t{test_name} <EXECUTE> - Execute tag matching : {{'asd'}}" + '\n'

    def test_no_tag_with_skip(self, plain_console_system_logger_on_trace):
        """
        GIVEN: config: no execute tags
        GIVEN: config: skip tag
        GIVEN: test: no tags
        WHEN: filter
        THEN: test filtered in
        """

        test_name = 'test_name'
        test_1 = Test(name=test_name, tags=[])

        filtered_tests = filter_tests_by_tags(system_logger=plain_console_system_logger_on_trace,
                                              config=Configuration(skip_tags=['asd']),
                                              tests=[test_1])

        assert filtered_tests == [test_1]

    def test_no_tag_with_skip_output(self,
                                     capsys,
                                     plain_console_system_logger_on_trace):
        """
        GIVEN: config: no execute tags
        GIVEN: config: skip tag
        GIVEN: test: no tags
        WHEN: filter
        THEN: log output = EXECUTE test
        """

        test_name = 'test_name'
        test_1 = Test(name=test_name, tags=[])

        filter_tests_by_tags(system_logger=plain_console_system_logger_on_trace,
                             config=Configuration(skip_tags=['asd']),
                             tests=[test_1])

        captured = capsys.readouterr()
        assert captured.out == '-' * 100 + '\n' \
               + 'Test files : filtering' + '\n' \
               + f'\t{test_name} <EXECUTE> - No skip tag matching' + '\n'

    def test_tag_matching_skip(self, plain_console_system_logger_on_trace):
        """
        GIVEN: config: no execute tags
        GIVEN: config: skip tag
        GIVEN: test: matching skip tag
        WHEN: filter
        THEN: test filtered out
        """

        test_name = 'test_name'
        test_1 = Test(name=test_name, tags=['asd'])

        filtered_tests = filter_tests_by_tags(system_logger=plain_console_system_logger_on_trace,
                                              config=Configuration(skip_tags=['asd']),
                                              tests=[test_1])

        assert filtered_tests == []

    def test_tag_matching_skip_output(self, capsys, plain_console_system_logger_on_trace):
        """
        GIVEN: config: no execute tags
        GIVEN: config: skip tag
        GIVEN: test: matching skip tag
        WHEN: filter
        THEN: log output = SKIP test
        """

        test_name = 'test_name'
        test_1 = Test(name=test_name, tags=['asd'])

        filter_tests_by_tags(system_logger=plain_console_system_logger_on_trace,
                             config=Configuration(skip_tags=['asd']),
                             tests=[test_1])

        captured = capsys.readouterr()
        assert captured.out == '-' * 100 + '\n' \
               + 'Test files : filtering' + '\n' \
               + f"\t{test_name} <SKIP> - Skip tag matching : {{'asd'}}" + '\n'

    def test_one_tag_matching_skip(self, plain_console_system_logger_on_trace):
        """
        GIVEN: config: no execute tags
        GIVEN: config: skip tag
        GIVEN: test: one matching skip tag
        WHEN: filter
        THEN: test filtered out
        """

        test_name = 'test_name'
        test_1 = Test(name=test_name, tags=['asd', 'asd2'])

        filtered_tests = filter_tests_by_tags(system_logger=plain_console_system_logger_on_trace,
                                              config=Configuration(skip_tags=['asd']),
                                              tests=[test_1])

        assert filtered_tests == []

    def test_one_tag_matching_skip(self, capsys, plain_console_system_logger_on_trace):
        """
        GIVEN: config: no execute tags
        GIVEN: config: skip tag
        GIVEN: test: one matching skip tag
        WHEN: filter
        THEN: test filtered out
        """

        test_name = 'test_name'
        test_1 = Test(name=test_name, tags=['asd', 'asd2'])

        filter_tests_by_tags(system_logger=plain_console_system_logger_on_trace,
                             config=Configuration(skip_tags=['asd']),
                             tests=[test_1])

        captured = capsys.readouterr()
        assert captured.out == '-' * 100 + '\n' \
               + 'Test files : filtering' + '\n' \
               + f"\t{test_name} <SKIP> - Skip tag matching : {{'asd'}}" + '\n'

    def test_tag_not_matching_skip(self, plain_console_system_logger_on_trace):
        """
        GIVEN: config: no execute tags
        GIVEN: config: skip tag
        GIVEN: test: tag not matching
        WHEN: filter
        THEN: test filtered in
        """

        test_name = 'test_name'
        test_1 = Test(name=test_name, tags=['asd2'])

        filtered_tests = filter_tests_by_tags(system_logger=plain_console_system_logger_on_trace,
                                              config=Configuration(skip_tags=['asd']),
                                              tests=[test_1])

        assert filtered_tests == [test_1]

    def test_tag_not_matching_output(self, capsys, plain_console_system_logger_on_trace):
        """
        GIVEN: config: no execute tags
        GIVEN: config: skip tag
        GIVEN: test: tag not matching
        WHEN: filter
        THEN: log output = EXECUTE test
        """

        test_name = 'test_name'
        test_1 = Test(name=test_name, tags=['asd2'])

        filter_tests_by_tags(system_logger=plain_console_system_logger_on_trace,
                             config=Configuration(skip_tags=['asd']),
                             tests=[test_1])

        captured = capsys.readouterr()
        assert captured.out == '-' * 100 + '\n' \
               + 'Test files : filtering' + '\n' \
               + f'\t{test_name} <EXECUTE> - No skip tag matching' + '\n'

    def test_matching_one_skip_tags(self, plain_console_system_logger_on_trace):
        """
        GIVEN: config: no execute tags
        GIVEN: config: skip tags
        GIVEN: test: matching one skip tag
        WHEN: filter
        THEN: test filtered out
        """

        test_name = 'test_name'
        test_1 = Test(name=test_name, tags=['asd'])

        filtered_tests = filter_tests_by_tags(system_logger=plain_console_system_logger_on_trace,
                                              config=Configuration(skip_tags=['asd', 'asd2']),
                                              tests=[test_1])

        assert filtered_tests == []

    def test_matching_one_skip_tags_output(self, capsys, plain_console_system_logger_on_trace):
        """
        GIVEN: config: no execute tags
        GIVEN: config: skip tags
        GIVEN: test: matching one skip tag
        WHEN: filter
        THEN: log output = SKIP
        """

        test_name = 'test_name'
        test_1 = Test(name=test_name, tags=['asd'])

        filter_tests_by_tags(system_logger=plain_console_system_logger_on_trace,
                             config=Configuration(skip_tags=['asd', 'asd2']),
                             tests=[test_1])

        captured = capsys.readouterr()
        assert captured.out == '-' * 100 + '\n' \
               + 'Test files : filtering' + '\n' \
               + f"\t{test_name} <SKIP> - Skip tag matching : {{'asd'}}" + '\n'

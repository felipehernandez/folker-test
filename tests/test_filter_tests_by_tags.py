from folker.cli import filter_tests_by_tags
from folker.model import Test
from folker.parameters import Configuration


class TestFilterTestByTags:
    def test_no_tags_no_filtering(self, capsys, plain_console_system_logger_on_trace):
        """
        GIVEN: config: no execute tags
        GIVEN: config: no skip tags
        GIVEN: test: no tags
        WHEN: filter
        THEN: test in
        THEN: log output = EXECUTE
        """

        test_name = 'exec: none, skip: none, test: none, in'
        test_1 = Test(name=test_name, tags=[])

        filtered_tests = filter_tests_by_tags(system_logger=plain_console_system_logger_on_trace,
                                              config=Configuration(),
                                              tests=[test_1])

        assert filtered_tests == [test_1]

        captured = capsys.readouterr()
        assert captured.out == '-' * 100 + '\n' \
               + 'Test files : filtering' + '\n' \
               + f'<EXECUTE> {test_name} - No tags restriction defined' + '\n'

    def test_tags_no_filtering(self, capsys, plain_console_system_logger_on_trace):
        """
        GIVEN: config: no execute tags
        GIVEN: config: no skip tags
        GIVEN: test: tag
        WHEN: filter
        THEN: test filtered in
        THEN: log output = EXECUTE
        """

        test_name = 'exec: none, skip: none, test: [a_tag], in'
        test_1 = Test(name=test_name, tags=['a_tag'])

        filtered_tests = filter_tests_by_tags(system_logger=plain_console_system_logger_on_trace,
                                              config=Configuration(),
                                              tests=[test_1])

        assert filtered_tests == [test_1]
        captured = capsys.readouterr()
        assert captured.out == '-' * 100 + '\n' \
               + 'Test files : filtering' + '\n' \
               + f'<EXECUTE> {test_name} - No tags restriction defined' + '\n'

    def test_no_tag_test_not_matching_execution_tags(self, capsys, plain_console_system_logger_on_trace):
        """
        GIVEN: config: execute tag
        GIVEN: config: no skip tags
        GIVEN: test: no tags
        WHEN: filter
        THEN: test filtered out
        THEN: log output = SKIP
        """

        test_name = 'exec: [a_tag], skip: none, test: none, out'
        test_1 = Test(name=test_name, tags=[])

        filtered_tests = filter_tests_by_tags(system_logger=plain_console_system_logger_on_trace,
                                              config=Configuration(tags=['a_tag']),
                                              tests=[test_1])

        assert filtered_tests == []
        captured = capsys.readouterr()
        assert captured.out == '-' * 100 + '\n' \
               + 'Test files : filtering' + '\n' \
               + f"<SKIP>    {test_name} - Missing execution tags : ['a_tag']" + '\n'

    def test_tagged_test_matching_execution_tags(self, capsys, plain_console_system_logger_on_trace):
        """
        GIVEN: config: execute tag
        GIVEN: config: no skip tags
        GIVEN: test: matching tag
        WHEN: filter
        THEN: test filtered in
        THEN: log output = EXECUTE
        """

        test_name = 'exec: [a_tag], skip: none, test: [a_tag], in'
        test_1 = Test(name=test_name, tags=['a_tag'])

        filtered_tests = filter_tests_by_tags(system_logger=plain_console_system_logger_on_trace,
                                              config=Configuration(tags=['a_tag']),
                                              tests=[test_1])

        assert filtered_tests == [test_1]
        captured = capsys.readouterr()
        assert captured.out == '-' * 100 + '\n' \
               + 'Test files : filtering' + '\n' \
               + f"<EXECUTE> {test_name} - Execute tag matching : ['a_tag']" + '\n'

    def test_tagged_test_not_matching_execution_tags(self, capsys, plain_console_system_logger_on_trace):
        """
        GIVEN: config: execute tag
        GIVEN: config: no skip tags
        GIVEN: test: not matching tag
        WHEN: filter
        THEN: test filtered out
        THEN: log output = SKIP
        """

        test_name = 'exec: [a_tag], skip: none, test: [another_tag], out'
        test_1 = Test(name=test_name, tags=['another_tag'])

        filtered_tests = filter_tests_by_tags(system_logger=plain_console_system_logger_on_trace,
                                              config=Configuration(tags=['a_tag']),
                                              tests=[test_1])

        assert filtered_tests == []
        captured = capsys.readouterr()
        assert captured.out == '-' * 100 + '\n' \
               + 'Test files : filtering' + '\n' \
               + f"<SKIP>    {test_name} - Missing execution tags : ['a_tag']" + '\n'

    def test_one_execution_tag_matching(self, capsys, plain_console_system_logger_on_trace):
        """
        GIVEN: config: execute tags
        GIVEN: config: no skip tags
        GIVEN: test: matching tags
        WHEN: filter
        THEN: test filtered in
        THEN: log output = SKIP
        """

        test_name = 'exec: [a_tag, another_tag], skip: none, test: [a_tag, another_tag], out'
        test_1 = Test(name=test_name, tags=['a_tag', 'another_tag'])

        filtered_tests = filter_tests_by_tags(system_logger=plain_console_system_logger_on_trace,
                                              config=Configuration(tags=['a_tag', 'another_tag']),
                                              tests=[test_1])

        assert filtered_tests == [test_1]
        captured = capsys.readouterr()
        assert captured.out == '-' * 100 + '\n' \
               + 'Test files : filtering' + '\n' \
               + f"<EXECUTE> {test_name} - Execute tag matching : ['a_tag', 'another_tag']" + '\n'

    def test_multiple_execution_tag_one_matching(self, capsys, plain_console_system_logger_on_trace):
        """
        GIVEN: config: multiple execute tags
        GIVEN: config: no skip tags
        GIVEN: test: one matching tags
        WHEN: filter
        THEN: test filtered out
        THEN: log output = SKIP test
        """

        test_name = 'exec: [a_tag, another_tag], skip: none, test: [a_tag], in'
        test_1 = Test(name=test_name, tags=['a_tag'])

        filtered_tests = filter_tests_by_tags(system_logger=plain_console_system_logger_on_trace,
                                              config=Configuration(tags=['a_tag', 'another_tag']),
                                              tests=[test_1])

        assert filtered_tests == []
        captured = capsys.readouterr()
        assert captured.out == '-' * 100 + '\n' \
               + 'Test files : filtering' + '\n' \
               + f"<SKIP>    {test_name} - Missing execution tags : ['another_tag']" + '\n'

    def test_no_tag_with_skip(self, capsys, plain_console_system_logger_on_trace):
        """
        GIVEN: config: no execute tags
        GIVEN: config: skip tag
        GIVEN: test: no tags
        WHEN: filter
        THEN: test filtered in
        THEN: log output = EXECUTE test
        """

        test_name = 'exec: none, skip: [a_tag], test: none, in'
        test_1 = Test(name=test_name, tags=[])

        filtered_tests = filter_tests_by_tags(system_logger=plain_console_system_logger_on_trace,
                                              config=Configuration(skip_tags=['a_tag']),
                                              tests=[test_1])

        assert filtered_tests == [test_1]
        captured = capsys.readouterr()
        assert captured.out == '-' * 100 + '\n' \
               + 'Test files : filtering' + '\n' \
               + f'<EXECUTE> {test_name} - No skip tag matching' + '\n'

    def test_tag_matching_skip(self, capsys, plain_console_system_logger_on_trace):
        """
        GIVEN: config: no execute tags
        GIVEN: config: skip tag
        GIVEN: test: matching skip tag
        WHEN: filter
        THEN: test filtered out
        THEN: log output = SKIP test
        """

        test_name = 'exec: none, skip: [a_tag], test: [a_tag], out'
        test_1 = Test(name=test_name, tags=['a_tag'])

        filtered_tests = filter_tests_by_tags(system_logger=plain_console_system_logger_on_trace,
                                              config=Configuration(skip_tags=['a_tag']),
                                              tests=[test_1])

        assert filtered_tests == []
        captured = capsys.readouterr()
        assert captured.out == '-' * 100 + '\n' \
               + 'Test files : filtering' + '\n' \
               + f"<SKIP>    {test_name} - Skip tag matching : ['a_tag']" + '\n'

    def test_one_tag_matching_skip(self, capsys, plain_console_system_logger_on_trace):
        """
        GIVEN: config: no execute tags
        GIVEN: config: skip tag
        GIVEN: test: one matching skip tag
        WHEN: filter
        THEN: test filtered out
        THEN: log output = SKIP
        """

        test_name = 'exec: none, skip: [a_tag], test: [a_tag, another_tag], out'
        test_1 = Test(name=test_name, tags=['a_tag', 'another_tag'])

        filtered_tests = filter_tests_by_tags(system_logger=plain_console_system_logger_on_trace,
                                              config=Configuration(skip_tags=['a_tag']),
                                              tests=[test_1])

        assert filtered_tests == []
        captured = capsys.readouterr()
        assert captured.out == '-' * 100 + '\n' \
               + 'Test files : filtering' + '\n' \
               + f"<SKIP>    {test_name} - Skip tag matching : ['a_tag']" + '\n'

    def test_tag_not_matching_skip(self, capsys, plain_console_system_logger_on_trace):
        """
        GIVEN: config: no execute tags
        GIVEN: config: skip tag
        GIVEN: test: tag not matching
        WHEN: filter
        THEN: test filtered in
        THEN: log output = EXECUTE test
        """

        test_name = 'exec: none, skip: [a_tag], test: [another_tag], in'
        test_1 = Test(name=test_name, tags=['another_tag'])

        filtered_tests = filter_tests_by_tags(system_logger=plain_console_system_logger_on_trace,
                                              config=Configuration(skip_tags=['a_tag']),
                                              tests=[test_1])

        assert filtered_tests == [test_1]
        captured = capsys.readouterr()
        assert captured.out == '-' * 100 + '\n' \
               + 'Test files : filtering' + '\n' \
               + f'<EXECUTE> {test_name} - No skip tag matching' + '\n'

    def test_matching_one_skip_tags(self, capsys, plain_console_system_logger_on_trace):
        """
        GIVEN: config: no execute tags
        GIVEN: config: skip tags
        GIVEN: test: matching one skip tag
        WHEN: filter
        THEN: test filtered out
        THEN: log output = SKIP
        """

        test_name = 'exec: none, skip: [a_tag, another_tag], test: [a_tag], out'
        test_1 = Test(name=test_name, tags=['a_tag'])

        filtered_tests = filter_tests_by_tags(system_logger=plain_console_system_logger_on_trace,
                                              config=Configuration(skip_tags=['a_tag', 'another_tag']),
                                              tests=[test_1])

        assert filtered_tests == []
        captured = capsys.readouterr()
        assert captured.out == '-' * 100 + '\n' \
               + 'Test files : filtering' + '\n' \
               + f"<SKIP>    {test_name} - Skip tag matching : ['a_tag']" + '\n'

    def test_one_execution_one_skip_tag_matching(self, capsys, plain_console_system_logger_on_trace):
        """
        GIVEN: config: execute tags
        GIVEN: config: skip tags
        GIVEN: test: matching tags
        WHEN: filter
        THEN: test filtered in
        THEN: log output = EXECUTE test
        """

        test_name = 'exec: [a_tag], skip: [another_tag], test: [a_tag, another_tag], out'
        test_1 = Test(name=test_name, tags=['a_tag', 'another_tag'])

        filtered_tests = filter_tests_by_tags(system_logger=plain_console_system_logger_on_trace,
                                              config=Configuration(tags=['a_tag'], skip_tags=['another_tag']),
                                              tests=[test_1])

        assert filtered_tests == []
        captured = capsys.readouterr()
        assert captured.out == '-' * 100 + '\n' \
               + 'Test files : filtering' + '\n' \
               + f"<SKIP>    {test_name} - Skip tag matching : ['another_tag']" + '\n'

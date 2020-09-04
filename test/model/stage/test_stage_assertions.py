from unittest import TestCase

from folker.logger.console_parallel_test_logger import ConsoleParallelTestLogger
from folker.model.context import Context
from folker.model.error.assertions import TestFailException, UnresolvableAssertionException, MalformedAssertionException
from folker.model.stage.assertions import StageAssertions


class TestStageAssertions(TestCase):
    stage: StageAssertions
    logger: ConsoleParallelTestLogger

    def setUp(self):
        self.stage = StageAssertions()
        self.logger = ConsoleParallelTestLogger()

    def test_given_no_assertions_then_no_execution(self):
        context = self.stage.execute(self.logger, Context())

        self.assertEqual({}, context.test_variables)
        self.assertEqual({}, context.stage_variables)

    def test_given_correct_passing_assertion_then_success(self):
        self.stage.assertions = ['1 + 1 == 2']

        context = self.stage.execute(self.logger, Context())

        self.assertEqual({}, context.test_variables)
        self.assertEqual({}, context.stage_variables)

    def test_given_correct_passing_assertion_with_variables_then_success(self):
        self.stage.assertions = ['${value} + 1 == 2']

        context = self.stage.execute(self.logger, Context({'value': 1}))

        self.assertEqual({'value': 1}, context.test_variables)
        self.assertEqual({}, context.stage_variables)

    def test_given_correct_failing_assertion_then_failure(self):
        self.stage.assertions = ['1 + 1 == 3']

        try:
            self.stage.execute(self.logger, Context())
            raise AssertionError('Should not get here')
        except TestFailException as test_fail_exception:
            self.assertEqual('AssertExecutor', test_fail_exception.source)
            self.assertEqual('Assertions failed', test_fail_exception.error)
            self.assertEqual('Assertions failed', test_fail_exception.cause)
            self.assertTrue('1 + 1 == 3' in test_fail_exception.details['errors'])

    def test_given_correct_failing_assertion_with_variables_then_failure(self):
        self.stage.assertions = ['${value} + 1 == 3']

        try:
            self.stage.execute(self.logger, Context({'value': 1}))
            raise AssertionError('Should not get here')
        except TestFailException as test_fail_exception:
            self.assertEqual('AssertExecutor', test_fail_exception.source)
            self.assertEqual('Assertions failed', test_fail_exception.error)
            self.assertEqual('Assertions failed', test_fail_exception.cause)
            self.assertTrue('${value} + 1 == 3' in test_fail_exception.details['errors'])

    def test_given_incorrect_assertion_then_malformed(self):
        self.stage.assertions = ['1 + 1']

        try:
            self.stage.execute(self.logger, Context({'value': 1}))
            raise AssertionError('Should not get here')
        except MalformedAssertionException as test_fail_exception:
            self.assertEqual('AssertExecutor', test_fail_exception.source)
            self.assertEqual('Malformed assertion', test_fail_exception.error)
            self.assertEqual('Assertion does not resolve to a True/False value', test_fail_exception.cause)
            self.assertTrue('1 + 1' in test_fail_exception.details['assertion'])

    def test_given_malformed_assertion_then_malformed(self):
        self.stage.assertions = ['1 + == 2']

        try:
            self.stage.execute(self.logger, Context({'value': 1}))
            raise AssertionError('Should not get here')
        except UnresolvableAssertionException as test_fail_exception:
            self.assertEqual('AssertExecutor', test_fail_exception.source)
            self.assertEqual('Malformed assertion', test_fail_exception.error)
            self.assertEqual('Assertion does not compile', test_fail_exception.cause)
            self.assertTrue('1 + == 2' in test_fail_exception.details['assertion'])

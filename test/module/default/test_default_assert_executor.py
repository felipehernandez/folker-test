from unittest import TestCase

from folker.logger.logger import TestLogger
from folker.model.data import StageData
from folker.model.error.assertions import TestFailException, MalformedAssertionException, UnresolvableAssertionException
from folker.module.default.assert_executor import DefaultAssertExecutor


class TestDefaultAssertExecutor(TestCase):

    def test_given_no_assertions_then_no_execution(self):
        executor = DefaultAssertExecutor()
        executor.set_logger(TestLogger())

        stage_data = StageData(
            id='default',
            name='stage_name'
        )

        test_context, stage_context = executor.execute(stage_data, {}, {})

        self.assertEqual({}, test_context)
        self.assertEqual({}, stage_context)

    def test_given_correct_passing_assertion_then_success(self):
        executor = DefaultAssertExecutor()
        executor.set_logger(TestLogger())

        stage_data = StageData(
            id='default',
            name='stage_name',
            assertions=['1 + 1 == 2']
        )

        test_context, stage_context = executor.execute(stage_data, {}, {})

        self.assertEqual({}, test_context)
        self.assertEqual({}, stage_context)

    def test_given_correct_passing_assertion_with_variables_then_success(self):
        executor = DefaultAssertExecutor()
        executor.set_logger(TestLogger())

        stage_data = StageData(
            id='default',
            name='stage_name',
            assertions=['${value} + 1 == 2']
        )

        test_context, stage_context = executor.execute(stage_data, {'value': 1}, {})

        self.assertEqual({'value': 1}, test_context)
        self.assertEqual({}, stage_context)

    def test_given_correct_failing_assertion_then_failure(self):
        executor = DefaultAssertExecutor()
        executor.set_logger(TestLogger())

        stage_data = StageData(
            id='default',
            name='stage_name',
            assertions=['1 + 1 == 3']
        )

        try:
            executor.execute(stage_data, {}, {})
            raise AssertionError('Should not get here')
        except TestFailException as test_fail_exception:
            self.assertEqual('AssertExecutor', test_fail_exception.source)
            self.assertEqual('Assertions failed', test_fail_exception.error)
            self.assertEqual('Assertions failed', test_fail_exception.cause)
            self.assertTrue('1 + 1 == 3' in test_fail_exception.details['errors'])

    def test_given_correct_failing_assertion_with_variables_then_failure(self):
        executor = DefaultAssertExecutor()
        executor.set_logger(TestLogger())

        stage_data = StageData(
            id='default',
            name='stage_name',
            assertions=['${value} + 1 == 3']
        )

        try:
            executor.execute(stage_data, {'value': 1}, {})
            raise AssertionError('Should not get here')
        except TestFailException as test_fail_exception:
            self.assertEqual('AssertExecutor', test_fail_exception.source)
            self.assertEqual('Assertions failed', test_fail_exception.error)
            self.assertEqual('Assertions failed', test_fail_exception.cause)
            self.assertTrue('${value} + 1 == 3' in test_fail_exception.details['errors'])

    def test_given_incorrect_assertion_then_malformed(self):
        executor = DefaultAssertExecutor()
        executor.set_logger(TestLogger())

        stage_data = StageData(
            id='default',
            name='stage_name',
            assertions=['1 + 1']
        )

        try:
            executor.execute(stage_data, {}, {})
            raise AssertionError('Should not get here')
        except MalformedAssertionException as test_fail_exception:
            self.assertEqual('AssertExecutor', test_fail_exception.source)
            self.assertEqual('Malformed assertion', test_fail_exception.error)
            self.assertEqual('Assertion does not resolve to a True/False value', test_fail_exception.cause)
            self.assertTrue('1 + 1' in test_fail_exception.details['assertion'])

    def test_given_malformed_assertion_then_malformed(self):
        executor = DefaultAssertExecutor()
        executor.set_logger(TestLogger())

        stage_data = StageData(
            id='default',
            name='stage_name',
            assertions=['1 + == 2']
        )

        try:
            executor.execute(stage_data, {}, {})
            raise AssertionError('Should not get here')
        except UnresolvableAssertionException as test_fail_exception:
            self.assertEqual('AssertExecutor', test_fail_exception.source)
            self.assertEqual('Malformed assertion', test_fail_exception.error)
            self.assertEqual('Assertion does not compile', test_fail_exception.cause)
            self.assertTrue('1 + == 2' in test_fail_exception.details['assertion'])

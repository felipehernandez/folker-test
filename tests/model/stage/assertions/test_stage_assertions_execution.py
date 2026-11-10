import pytest

from folker.logger import TestLogger
from folker.logger.test_logger import PlainConsoleParallelTestLogger
from folker.model.context import Context
from folker.model.error.assertions import TestFailException, MalformedAssertionException, \
    UnresolvableAssertionException
from folker.model.stage.assertions import StageAssertions
from folker.parameters import Configuration


class TestStageAssertions:
    logger: TestLogger = PlainConsoleParallelTestLogger(Configuration())

    def test_given_no_assertions_then_no_execution(self):
        stage = StageAssertions(assertions=[])

        context = stage.execute(self.logger, Context())

        assert {} == context.test_variables
        assert {} == context.stage_variables

    def test_given_correct_passing_assertion_then_success(self):
        stage = StageAssertions(assertions=['1 + 1 == 2'])

        context = stage.execute(self.logger, Context())

        assert {} == context.test_variables
        assert {} == context.stage_variables

    def test_given_correct_passing_assertion_with_variables_then_success(self):
        stage = StageAssertions(assertions=['${value} + 1 == 2'])

        context = stage.execute(self.logger, Context({'value': 1}))

        assert {'value': 1} == context.test_variables
        assert {} == context.stage_variables

    def test_given_correct_failing_assertion_then_failure(self):
        stage = StageAssertions(assertions=['1 + 1 == 3'])

        with pytest.raises(TestFailException) as test_fail_exception:
            stage.execute(self.logger, Context())

        assert test_fail_exception.value.source == 'AssertExecutor'
        assert test_fail_exception.value.error == 'Assertions failed'
        assert test_fail_exception.value.cause == 'Assertions failed'
        assert '1 + 1 == 3' in test_fail_exception.value.details['errors']

    def test_given_correct_failing_assertion_with_variables_then_failure(self):
        stage = StageAssertions(assertions=['${value} + 1 == 3'])

        with pytest.raises(TestFailException) as test_fail_exception:
            stage.execute(self.logger, Context({'value': 1}))

        assert test_fail_exception.value.source == 'AssertExecutor'
        assert test_fail_exception.value.error == 'Assertions failed'
        assert test_fail_exception.value.cause == 'Assertions failed'
        assert '${value} + 1 == 3' in test_fail_exception.value.details['errors']

    def test_given_incorrect_assertion_then_malformed(self):
        stage = StageAssertions(assertions=['1 + 1'])

        with pytest.raises(MalformedAssertionException) as test_fail_exception:
            stage.execute(self.logger, Context({'value': 1}))

        assert test_fail_exception.value.source == 'AssertExecutor'
        assert test_fail_exception.value.error == 'Malformed assertion'
        assert test_fail_exception.value.cause == 'Assertion does not resolve to a True/False value'
        assert '1 + 1' in test_fail_exception.value.details['assertion']

    def test_given_malformed_assertion_then_malformed(self):
        stage = StageAssertions(assertions=['1 + == 2'])

        with pytest.raises(UnresolvableAssertionException) as test_fail_exception:
            stage.execute(self.logger, Context({'value': 1}))

        assert test_fail_exception.value.source == 'AssertExecutor'
        assert test_fail_exception.value.error == 'Malformed assertion'
        assert test_fail_exception.value.cause == 'Assertion does not compile'
        assert '1 + == 2' in test_fail_exception.value.details['assertion']


# BUG-09: `success is not executed` compared ints by identity. CPython only caches the ints
# -5..256, so with more assertions than that two equal counts were reported as different.
class TestStageAssertionsWithManyAssertions:
    logger: TestLogger = PlainConsoleParallelTestLogger(Configuration())

    def test_given_more_than_256_passing_assertions_then_success(self):
        stage = StageAssertions(assertions=['1 == 1'] * 300)

        context = stage.execute(self.logger, Context())

        assert {} == context.test_variables

    def test_given_more_than_256_assertions_and_one_failing_then_only_it_fails(self):
        stage = StageAssertions(assertions=['1 == 1'] * 299 + ['1 == 2'])

        with pytest.raises(TestFailException) as test_fail_exception:
            stage.execute(self.logger, Context())

        assert test_fail_exception.value.details['errors'] == ['1 == 2']

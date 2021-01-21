import pytest

from folker.logger.console_parallel_test_logger import ConsoleParallelTestLogger
from folker.model.context import Context
from folker.model.error.assertions import TestFailException, MalformedAssertionException, \
    UnresolvableAssertionException
from folker.model.stage.assertions import StageAssertions


class TestStageAssertions:
    stage: StageAssertions
    logger: ConsoleParallelTestLogger

    @pytest.fixture(autouse=True)
    def setup(self):
        self.stage = StageAssertions()
        self.logger = ConsoleParallelTestLogger()
        yield

    def test_given_no_assertions_then_no_execution(self):
        context = self.stage.execute(self.logger, Context())

        assert {} == context.test_variables
        assert {} == context.stage_variables

    def test_given_correct_passing_assertion_then_success(self):
        self.stage.assertions = ['1 + 1 == 2']

        context = self.stage.execute(self.logger, Context())

        assert {} == context.test_variables
        assert {} == context.stage_variables

    def test_given_correct_passing_assertion_with_variables_then_success(self):
        self.stage.assertions = ['${value} + 1 == 2']

        context = self.stage.execute(self.logger, Context({'value': 1}))

        assert {'value': 1} == context.test_variables
        assert {} == context.stage_variables

    def test_given_correct_failing_assertion_then_failure(self):
        self.stage.assertions = ['1 + 1 == 3']

        with pytest.raises(TestFailException) as test_fail_exception:
            self.stage.execute(self.logger, Context())

        assert test_fail_exception.value.source == 'AssertExecutor'
        assert test_fail_exception.value.error == 'Assertions failed'
        assert test_fail_exception.value.cause == 'Assertions failed'
        assert '1 + 1 == 3' in test_fail_exception.value.details['errors']

    def test_given_correct_failing_assertion_with_variables_then_failure(self):
        self.stage.assertions = ['${value} + 1 == 3']

        with pytest.raises(TestFailException) as test_fail_exception:
            self.stage.execute(self.logger, Context({'value': 1}))

        assert test_fail_exception.value.source == 'AssertExecutor'
        assert test_fail_exception.value.error == 'Assertions failed'
        assert test_fail_exception.value.cause == 'Assertions failed'
        assert '${value} + 1 == 3' in test_fail_exception.value.details['errors']

    def test_given_incorrect_assertion_then_malformed(self):
        self.stage.assertions = ['1 + 1']

        with pytest.raises(MalformedAssertionException) as test_fail_exception:
            self.stage.execute(self.logger, Context({'value': 1}))

        assert test_fail_exception.value.source == 'AssertExecutor'
        assert test_fail_exception.value.error == 'Malformed assertion'
        assert test_fail_exception.value.cause == 'Assertion does not resolve to a True/False value'
        assert '1 + 1' in test_fail_exception.value.details['assertion']

    def test_given_malformed_assertion_then_malformed(self):
        self.stage.assertions = ['1 + == 2']

        with pytest.raises(UnresolvableAssertionException) as test_fail_exception:
            self.stage.execute(self.logger, Context({'value': 1}))

        assert test_fail_exception.value.source == 'AssertExecutor'
        assert test_fail_exception.value.error == 'Malformed assertion'
        assert test_fail_exception.value.cause == 'Assertion does not compile'
        assert '1 + == 2' in test_fail_exception.value.details['assertion']

    def test_enrich(self):
        stage = StageAssertions(assertions=['assertion1'])
        template_stage = StageAssertions(assertions=['assertion2'])

        stage.enrich(template_stage)

        assert stage.assertions == ['assertion1', 'assertion2']

    def test_validate(self):
        stage = StageAssertions()

        stage.validate()

    def test_validate_empty(self):
        stage = StageAssertions(assertions=['assertion1'])

        stage.validate()

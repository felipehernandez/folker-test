from copy import copy

from folker.logger.logger import TestLogger
from folker.model.context import Context
from folker.model.error.assertions import UnresolvableAssertionException, MalformedAssertionException, TestFailException
from folker.model.stage.stage import StageStep


class StageAssertions(StageStep):
    assertions: [str]

    def __init__(self, assertions: [str] = []) -> None:
        super().__init__()
        self.assertions = assertions

    def enrich(self, template: 'StageAssertions'):
        new_data = []
        new_data.extend(self.assertions + template.assertions)
        self.assertions = new_data

    def validate(self):
        pass

    def __copy__(self):
        return copy(self)

    def execute(self, logger: TestLogger, context: Context) -> Context:
        assertion_definitions = self.assertions

        if len(assertion_definitions) == 0:
            return context

        executed, success, failures = 0, 0, []
        for assertion_definition in assertion_definitions:
            executed += 1

            assert_result = self._assert_individual(logger, assertion_definition, context)

            if assert_result:
                success += 1
            else:
                failures.append(assertion_definition)

        self._wrap_up_test(logger, executed, success, failures)

        return context

    def _assert_individual(self, logger: TestLogger, assertion: str, context: Context) -> (bool, dict):
        updated_assertion, variables = context.map_variables(assertion)

        try:
            result = eval(updated_assertion, {'variables': variables})
        except Exception as e:
            logger.assertion_error(assertion=assertion, exception=e)
            raise UnresolvableAssertionException(assertion=assertion)

        if not isinstance(result, bool):
            raise MalformedAssertionException(assertion=assertion)

        if result:
            logger.assertion_success(assertion=assertion)
        else:
            logger.assertion_fail(assertion=assertion, variables=variables)

        return result

    def _wrap_up_test(self, logger: TestLogger, executed, success, failures):
        logger.assert_test_result(executed, success, executed - success)
        if success is not executed:
            raise TestFailException(failure_messages=failures)

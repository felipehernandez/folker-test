from copy import copy

from folker.logger.logger import TestLogger
from folker.model.error.assertions import UnresolvableAssertionException, MalformedAssertionException, TestFailException
from folker.model.stage.stage import StageStep
from folker.util.variable import map_variables


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

    def execute(self, logger: TestLogger, test_context: dict, stage_context: dict) -> (dict, dict):
        assertion_definitions = self.assertions

        if len(assertion_definitions) == 0:
            return test_context, stage_context

        executed, success, failures = 0, 0, []
        for assertion_definition in assertion_definitions:
            executed += 1

            assert_result = self._assert_individual(logger, assertion_definition, test_context, stage_context)

            if assert_result:
                success += 1
            else:
                failures.append(assertion_definition)

        self._wrap_up_test(logger, executed, success, failures)

        return test_context, stage_context

    def _assert_individual(self, logger: TestLogger, assertion: str, test_context: dict, stage_context: dict) -> (bool, dict):
        updated_assertion, variables = map_variables(test_context, stage_context, assertion)

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

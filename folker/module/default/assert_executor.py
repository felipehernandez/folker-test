from folker.model.data import StageData
from folker.model.error.assertions import TestFailException, MalformedAssertionException, UnresolvableAssertionException
from folker.model.task import AssertExecutor
from folker.util.variable import map_variables


class DefaultAssertExecutor(AssertExecutor):

    def execute(self, stage_data: StageData, test_context: dict, stage_context: dict) -> (dict, dict):
        assertion_definitions = stage_data.assertions.assertions

        if len(assertion_definitions) is 0:
            return test_context, stage_context

        executed, success, failures = 0, 0, []
        for assertion_definition in assertion_definitions:
            executed += 1

            assert_result = self._assert_individual(assertion_definition, test_context, stage_context)

            if assert_result:
                success += 1
            else:
                failures.append(assertion_definition)

        self.wrap_up_test(executed, success, failures)

        return test_context, stage_context

    def _assert_individual(self, assertion: str, test_context: dict, stage_context: dict) -> (bool, dict):
        updated_assertion, variables = map_variables(test_context, stage_context, assertion)

        try:
            result = eval(updated_assertion)
        except Exception as e:
            self.logger.assertion_error(assertion=assertion, exception=e)
            raise UnresolvableAssertionException(assertion=assertion)

        if not isinstance(result, bool):
            raise MalformedAssertionException(assertion=assertion)

        if result:
            self.logger.assertion_success(assertion=assertion)
        else:
            self.logger.assertion_fail(assertion=assertion, variables=variables)

        return result

    def wrap_up_test(self, executed, success, failures):
        self.logger.assert_test_result(executed, success, executed - success)
        if success is not executed:
            raise TestFailException(failure_messages=failures)

from abc import abstractmethod
from copy import copy

from folker.logger.logger import TestLogger
from folker.model.error.assertions import UnresolvableAssertionException, MalformedAssertionException, TestFailException
from folker.model.error.error import SourceException
from folker.util.variable import replace_variables, map_variables


class Action:

    @abstractmethod
    def execute(self, logger: TestLogger, test_context: dict, stage_context: dict) -> (dict, dict):
        pass


class StageSave:
    save: dict

    def __init__(self, save: dict = {}) -> None:
        super().__init__()
        self.save = save if save else {}

    def enrich(self, save: dict = {}):
        new_data = StageSave()
        new_data.save = {}
        new_data.save = {**self.save, **save}
        return new_data

    def __copy__(self):
        return copy(self)

    def execute(self, logger: TestLogger, test_context: dict, stage_context: dict) -> (dict, dict):
        for (variable, saving) in self.save.items():
            try:
                updated_assertion, variables = map_variables(test_context, stage_context, saving)
                test_context[variable] = eval(updated_assertion)
            except Exception as e:
                test_context[variable] = replace_variables(test_context={}, stage_context=stage_context, text=saving)

        return test_context, stage_context


class StageLog:
    logs: [str]

    def __init__(self, logs: [str] = []) -> None:
        super().__init__()
        self.logs = logs if logs else []

    def extend(self, logs: [str] = []):
        new_data = StageLog()
        new_data.logs = []
        new_data.logs.extend(self.logs + logs)
        return new_data

    def execute(self, logger: TestLogger, test_context: dict, stage_context: dict) -> (dict, dict):
        for log in self.logs:
            logger.log_text(replace_variables(test_context, stage_context, log))

        return test_context, stage_context


class StageAssertions:
    assertions: [str]

    def __init__(self, assertions: [str] = []) -> None:
        super().__init__()
        self.assertions = assertions

    def enrich(self, assertions: [str] = []):
        new_data = StageAssertions()
        new_data.assertions = []
        new_data.assertions.extend(self.assertions + assertions)
        return new_data

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
            result = eval(updated_assertion)
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


class Stage:
    id: str
    name: str

    action: Action

    save: StageSave
    log: StageLog
    assertions: StageAssertions

    def __init__(self,
                 id: str = None,
                 name: str = None,
                 action: Action = None,
                 log: [str] = None,
                 save: dict = None,
                 assertions: [str] = [],
                 **kwargs) -> None:
        super().__init__()
        self.id = id
        self.name = name

        self.action = action
        self.save = StageSave(save)
        self.log = StageLog(log)
        self.assertions = StageAssertions(assertions)

    def execute(self, logger: TestLogger, test_context: dict):
        stage_context = {}
        logger.stage_start(self.name, test_context)

        try:
            test_context, stage_context = self.action.execute(logger=logger, test_context=test_context, stage_context=stage_context)
            logger.action_executed(stage_context)
            test_context, stage_context = self.save.execute(logger=logger, test_context=test_context, stage_context=stage_context)
            test_context, stage_context = self.log.execute(logger=logger, test_context=test_context, stage_context=stage_context)
            test_context, stage_context = self.assertions.execute(logger=logger, test_context=test_context, stage_context=stage_context)
        except SourceException as e:
            e.details['stage'] = self
            raise e

        return test_context


class Test:
    name: str
    description: str
    parallel: bool

    stages: [Stage]

    def __init__(self,
                 name: str = 'UNDEFINED',
                 description: str = None,
                 parallel: bool = False,
                 stages: [Stage] = []
                 ) -> None:
        super().__init__()
        self.name = name
        self.description = description
        self.parallel = parallel
        self.stages = stages

    def execute(self, logger: TestLogger, test_context: dict = None):
        if test_context is None:
            test_context = dict()

        logger.test_start(self.name, self.description)
        try:
            for stage in self.stages:
                test_context = stage.execute(logger, test_context)
        except SourceException as e:
            logger.test_finish_error(e)
            return False

        logger.test_finish()

        return True

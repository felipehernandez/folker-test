from folker import logger
from folker.model.data import StageData
from folker.model.error.error import SourceException
from folker.model.task import ActionExecutor, AssertExecutor, SaveExecutor, LogExecutor


class StageExecutors:
    action: ActionExecutor
    assertion: AssertExecutor
    save: SaveExecutor
    log: LogExecutor

    def __init__(self,
                 action: ActionExecutor,
                 assertion: AssertExecutor,
                 save: SaveExecutor,
                 log: LogExecutor) -> None:
        super().__init__()

        self.action = action
        self.assertion = assertion
        self.save = save
        self.log = log


class Stage:
    data: StageData
    executors: StageExecutors

    def __init__(self, data: StageData = None, executors: StageExecutors = None) -> None:
        super().__init__()
        self.data = data
        self.executors = executors

    def execute(self, test_ctxt: dict):
        stage_ctxt = {}
        logger.stage_start(self.data)

        try:
            test_ctxt, stage_ctxt = self.executors.action.execute(stage_data=self.data, test_context=test_ctxt, stage_context=stage_ctxt)
            test_ctxt, stage_ctxt = self.executors.assertion.execute(stage_data=self.data, test_context=test_ctxt, stage_context=stage_ctxt)
            test_ctxt, stage_ctxt = self.executors.save.execute(stage_data=self.data, test_context=test_ctxt, stage_context=stage_ctxt)
            test_ctxt, stage_ctxt = self.executors.log.execute(stage_data=self.data, test_context=test_ctxt, stage_context=stage_ctxt)
        except SourceException as e:
            e.details['stage'] = self.data
            raise e

        return test_ctxt


class Test:
    name: str
    description: str
    stages: [Stage]

    def __init__(self,
                 test_name='UNDEFINED',
                 test_description='None',
                 stages: [Stage] = None) -> None:
        super().__init__()
        self.name = test_name
        self.description = test_description
        self.stages = stages

    def execute(self):
        logger.test_start(self.name, self.description)
        test_context = dict()
        try:
            for stage in self.stages:
                test_context = stage.execute(test_context)
        except SourceException as e:
            logger.stage_exception(e)

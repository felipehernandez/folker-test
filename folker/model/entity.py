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
        logger.stage_start(self.data, test_ctxt)

        try:
            test_ctxt, stage_ctxt = self.executors.action.execute(stage_data=self.data, test_context=test_ctxt, stage_context=stage_ctxt)
            logger.action_executed(stage_ctxt)
            test_ctxt, stage_ctxt = self.executors.log.execute(stage_data=self.data, test_context=test_ctxt, stage_context=stage_ctxt)
            test_ctxt, stage_ctxt = self.executors.save.execute(stage_data=self.data, test_context=test_ctxt, stage_context=stage_ctxt)
            test_ctxt, stage_ctxt = self.executors.assertion.execute(stage_data=self.data, test_context=test_ctxt, stage_context=stage_ctxt)
        except SourceException as e:
            e.details['stage'] = self.data
            raise e

        return test_ctxt

    def enrich(self, args: dict):
        return Stage(data=self.data.enrich(args), executors=self.executors)


class Test:
    name: str
    description: str
    stages: [Stage]

    def __init__(self,
                 name='UNDEFINED',
                 description='None',
                 stages: [Stage] = None) -> None:
        super().__init__()
        self.name = name
        self.description = description
        self.stages = stages

    def execute(self) -> bool:
        logger.test_start(self.name, self.description)
        test_context = dict()
        try:
            for stage in self.stages:
                test_context = stage.execute(test_context)
        except SourceException as e:
            logger.stage_exception(e)
            return False

        return True


class Template:
    id: str
    description: str
    stages: [Stage]

    def __init__(self,
                 id='UNDEFINED',
                 description='None',
                 stages: [Stage] = None) -> None:
        super().__init__()
        self.id = id
        self.description = description
        self.stages = stages

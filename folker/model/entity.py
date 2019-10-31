from folker.logger import Logger
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

    def set_logger(self, logger: Logger):
        self.action.set_logger(logger)
        self.assertion.set_logger(logger)
        self.save.set_logger(logger)
        self.log.set_logger(logger)


class Stage:
    data: StageData
    executors: StageExecutors

    logger: Logger

    def __init__(self, data: StageData = None, executors: StageExecutors = None) -> None:
        super().__init__()
        self.data = data
        self.executors = executors

    def set_logger(self, logger: Logger):
        self.logger = logger
        self.executors.set_logger(logger)

    def execute(self, test_ctxt: dict):
        stage_ctxt = {}
        self.logger.stage_start(self.data, test_ctxt)

        try:
            test_ctxt, stage_ctxt = self.executors.action.execute(stage_data=self.data, test_context=test_ctxt, stage_context=stage_ctxt)
            self.logger.action_executed(stage_ctxt)
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

    logger: Logger

    def __init__(self,
                 name='UNDEFINED',
                 description='None',
                 stages: [Stage] = None) -> None:
        super().__init__()
        self.name = name
        self.description = description
        self.stages = stages

    def set_logger(self, logger: Logger):
        self.logger = logger
        for stage in self.stages:
            stage.set_logger(logger)

    def execute(self) -> bool:
        self.logger.test_start(self.name, self.description)
        test_context = dict()
        try:
            for stage in self.stages:
                test_context = stage.execute(test_context)
        except SourceException as e:
            self.logger.stage_exception(e)
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

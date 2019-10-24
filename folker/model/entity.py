from folker.model import StageData
from folker.model.task import ActionExecutor, AssertExecutor


class StageExecutors:
    action: ActionExecutor
    assertion: AssertExecutor


class Stage:
    data: StageData
    executors: StageExecutors

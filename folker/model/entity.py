from folker.model import StageData
from folker.model.task import ActionExecutor, AssertExecutor, SaveExecutor, LogExecutor


class StageExecutors:
    action: ActionExecutor
    assertion: AssertExecutor
    save: SaveExecutor
    log: LogExecutor


class Stage:
    data: StageData
    executors: StageExecutors

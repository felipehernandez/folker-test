from abc import abstractmethod, ABC

from folker.logger import Logger
from folker.model.data import StageData


class TaskExecutor(ABC):
    logger: Logger

    def set_logger(self, logger: Logger):
        self.logger = logger

    @abstractmethod
    def execute(self, stage_data: StageData, test_context: dict, stage_context: dict) -> (dict, dict):
        return test_context, stage_context


class ActionExecutor(TaskExecutor, ABC):
    pass


class AssertExecutor(TaskExecutor, ABC):
    pass


class SaveExecutor(TaskExecutor, ABC):
    pass


class LogExecutor(TaskExecutor, ABC):
    pass

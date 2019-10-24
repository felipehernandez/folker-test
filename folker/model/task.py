from abc import abstractmethod, ABC

from folker.model.data import StageData


class TaskExecutor(ABC):
    @abstractmethod
    def execute(self, stage_data: StageData, test_context: dict, stage_context: dict) -> (dict, dict):
        pass


class ActionExecutor(TaskExecutor, ABC):
    pass


class AssertExecutor(TaskExecutor, ABC):
    pass


class SaveExecutor(TaskExecutor, ABC):
    pass

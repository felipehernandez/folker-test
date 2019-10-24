from folker.model.data import StageData
from folker.model.task import ActionExecutor


class DefaultActionExecutor(ActionExecutor):
    def execute(self, stage_data: StageData, test_context: dict, stage_context: dict) -> (dict, dict):
        return test_context, stage_context

from folker.model.data import ActionData
from folker.model.task import ActionExecutor


class DefaultActionExecutor(ActionExecutor):
    def execute(self, action_data: ActionData, test_context: dict, stage_context: dict) -> (dict, dict):
        return test_context, stage_context

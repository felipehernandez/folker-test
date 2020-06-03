from folker.logger.logger import TestLogger
from folker.model.entity import Action
from folker.util.decorator import timed_action, resolvable_variables, loggable


class PrintAction(Action):
    message: str

    def __init__(self, message: str = None, **kargs) -> None:
        super().__init__()
        self.message = message

    def mandatory_fields(self):
        return [
            'message'
        ]

    @loggable
    @resolvable_variables
    @timed_action
    def execute(self, logger: TestLogger, test_context: dict, stage_context: dict) -> (dict, dict):
        logger.message(self.message)

        return test_context, stage_context

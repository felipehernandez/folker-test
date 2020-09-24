from folker.logger import TestLogger
from folker.model import Context
from folker.model import StageAction
from folker.decorator import timed_action, resolvable_variables, loggable_action


class PrintStageAction(StageAction):
    message: str

    def __init__(self, message: str = None, **kargs) -> None:
        super().__init__()
        self.message = message

    def mandatory_fields(self):
        return [
            'message'
        ]

    @loggable_action
    @resolvable_variables
    @timed_action
    def execute(self, logger: TestLogger, context: Context) -> Context:
        logger.message(self.message)

        return context

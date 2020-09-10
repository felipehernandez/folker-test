from folker.logger.logger import TestLogger
from folker.model.context import Context
from folker.model.stage.action import Action
from folker.util.decorator import timed_action, loggable, resolvable_variables


class VoidAction(Action):

    def __init__(self, **kargs) -> None:
        super().__init__()

    def mandatory_fields(self) -> [str]:
        return []

    @loggable
    @resolvable_variables
    @timed_action
    def execute(self, logger: TestLogger, context: Context) -> Context:
        return context

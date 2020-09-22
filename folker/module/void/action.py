from folker.logger import TestLogger
from folker.model import Context
from folker.model import Action
from folker.decorator import timed_action, loggable_action, resolvable_variables


class VoidAction(Action):

    def __init__(self, **kargs) -> None:
        super().__init__()

    def mandatory_fields(self) -> [str]:
        return []

    @loggable_action
    @resolvable_variables
    @timed_action
    def execute(self, logger: TestLogger, context: Context) -> Context:
        return context

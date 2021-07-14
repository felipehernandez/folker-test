from folker.decorator import timed_action, loggable_action, resolvable_variables
from folker.logger import TestLogger
from folker.model import Context
from folker.model import StageAction


class VoidStageAction(StageAction):

    def __init__(self, **kargs) -> None:
        super().__init__()

    def __add__(self, template: 'StageAction'):
        pass

    def mandatory_fields(self) -> [str]:
        return []

    @loggable_action
    @resolvable_variables
    @timed_action
    def execute(self, logger: TestLogger, context: Context) -> Context:
        return context

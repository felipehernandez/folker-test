import time

from folker.logger.logger import TestLogger
from folker.model.context import Context
from folker.model.stage.action import Action
from folker.util.decorator import timed_action, resolvable_variables, loggable


class WaitAction(Action):
    time: float

    def __init__(self, time: str = None, **kargs) -> None:
        super().__init__()
        self.time = time

    def mandatory_fields(self) -> [str]:
        return ['time']

    @loggable
    @resolvable_variables
    @timed_action
    def execute(self, logger: TestLogger, context: Context) -> Context:
        time.sleep(float(self.time))
        return context

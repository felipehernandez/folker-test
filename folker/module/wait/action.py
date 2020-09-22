import time

from folker.decorator import loggable_action, resolvable_variables, timed_action
from folker.logger import TestLogger
from folker.model import Action
from folker.model import Context


class WaitAction(Action):
    time: float

    def __init__(self, time: str = None, **kargs) -> None:
        super().__init__()
        self.time = time

    def mandatory_fields(self) -> [str]:
        return ['time']

    @loggable_action
    @resolvable_variables
    @timed_action
    def execute(self, logger: TestLogger, context: Context) -> Context:
        time.sleep(float(self.time))
        return context

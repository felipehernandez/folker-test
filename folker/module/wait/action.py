import time

from folker.logger.logger import TestLogger
from folker.model.entity import Action
from folker.util.decorator import timed_action, resolvable_variables


class WaitAction(Action):
    time: float

    def __init__(self, time: str = None, **kargs) -> None:
        super().__init__()
        self.time = time

    def mandatory_fields(self) -> [str]:
        return ['time']

    @resolvable_variables
    @timed_action
    def execute(self, logger: TestLogger, test_context: dict, stage_context: dict) -> (dict, dict):
        time.sleep(float(self.time))
        return test_context, stage_context

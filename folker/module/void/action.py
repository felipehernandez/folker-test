from copy import deepcopy

from folker.logger.logger import TestLogger
from folker.model.entity import Action
from folker.util.decorator import timed_action


class VoidAction(Action):

    def __init__(self, **kargs) -> None:
        super().__init__()

    def enrich(self, template: 'VoidAction'):
        pass

    def validate(self):
        pass

    @timed_action
    def execute(self, logger: TestLogger, test_context: dict, stage_context: dict) -> (dict, dict):
        return test_context, stage_context

    def __copy__(self):
        return deepcopy(self)

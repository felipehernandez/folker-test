import time
from copy import deepcopy

from folker.logger.logger import TestLogger
from folker.model.entity import Action
from folker.model.error.load import InvalidSchemaDefinitionException
from folker.util.decorator import timed_action


class WaitAction(Action):
    time: float

    def __init__(self, time: float = None, **kargs) -> None:
        super().__init__()
        self.time = time

    def __copy__(self):
        return deepcopy(self)

    def enrich(self, template: 'WaitAction'):
        self._set_attribute_if_missing('time', template)

    def validate(self):
        missing_fields = []

        if not hasattr(self, 'time') or not self.time:
            missing_fields.append('action.time')

        if len(missing_fields) > 0:
            raise InvalidSchemaDefinitionException(missing_fields=missing_fields)

    @timed_action
    def execute(self, logger: TestLogger, test_context: dict, stage_context: dict) -> (dict, dict):
        time.sleep(self.time)
        return test_context, stage_context

import time
from copy import deepcopy

from folker.logger.logger import TestLogger
from folker.model.entity import Action
from folker.model.error.load import InvalidSchemaDefinitionException


class WaitAction(Action):
    time: float

    def __init__(self, time: float = None, **kargs) -> None:
        super().__init__()
        self.time = time

    def __copy__(self):
        return deepcopy(self)

    def enrich(self, template: 'WaitAction'):
        if self.time is None:
            self.time = template.time

    def validate(self):
        missing_fields = []

        if not hasattr(self, 'time') or not self.time:
            missing_fields.append('action.time')

        if len(missing_fields) > 0:
            raise InvalidSchemaDefinitionException(missing_fields=missing_fields)

    def execute(self, logger: TestLogger, test_context: dict, stage_context: dict) -> (dict, dict):
        start = time.time()

        time.sleep(self.time)

        end = time.time()
        stage_context['elapsed_time'] = int((end - start) * 1000)

        return test_context, stage_context

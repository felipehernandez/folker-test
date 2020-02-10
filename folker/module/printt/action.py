import time
from copy import deepcopy

from folker.logger.logger import TestLogger
from folker.model.entity import Action
from folker.model.error.load import InvalidSchemaDefinitionException
from folker.util.variable import replace_variables


class PrintAction(Action):
    message: str

    def __init__(self, message: str = None, **kargs) -> None:
        super().__init__()
        self.message = message

    def __copy__(self):
        return deepcopy(self)

    def enrich(self, template: 'PrintAction'):
        if self.message == None:
            self.message = template.message

    def validate(self):
        missing_fields = []

        if not hasattr(self, 'message') or not self.message:
            missing_fields.append('action.message')

        if len(missing_fields) > 0:
            raise InvalidSchemaDefinitionException(missing_fields=missing_fields)

    def execute(self, logger: TestLogger, test_context: dict, stage_context: dict) -> (dict, dict):
        start = time.time()

        message = replace_variables(test_context, stage_context, self.message)
        logger.message(message)

        end = time.time()
        stage_context['elapsed_time'] = int((end - start) * 1000)

        return test_context, stage_context

    def __copy__(self):
        return deepcopy(self)

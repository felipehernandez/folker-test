import time
from copy import deepcopy

from folker.logger.logger import TestLogger
from folker.model.entity import Action
from folker.model.error.load import InvalidSchemaDefinitionException


class CodeAction(Action):
    module: str
    method: str
    parameters: dict

    def __init__(self,
                 module: str = None,
                 method: str = None,
                 parameters: dict = None,
                 **kargs) -> None:
        super().__init__()
        self.module = module
        self.method = method
        self.parameters = parameters

    def __copy__(self):
        return deepcopy(self)

    def enrich(self, template: 'CodeAction'):
        self._set_attribute_if_missing(template, 'package')
        self._set_attribute_if_missing(template, 'method')
        self._set_attribute_if_missing(template, 'parameters')

    def validate(self):
        missing_fields = []

        if not hasattr(self, 'module') or not self.module:
            missing_fields.append('action.module')
        if not hasattr(self, 'method') or not self.method:
            missing_fields.append('action.method')

        if len(missing_fields) > 0:
            raise InvalidSchemaDefinitionException(missing_fields=missing_fields)

    def execute(self, logger: TestLogger, test_context: dict, stage_context: dict) -> (dict, dict):
        start = time.time()

        module = __import__(self.module, fromlist=[self.method])
        method = getattr(module, self.method)
        result = method(**self.parameters)

        stage_context['result'] = result

        end = time.time()
        stage_context['elapsed_time'] = int((end - start) * 1000)

        return test_context, stage_context

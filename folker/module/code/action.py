from folker.logger.logger import TestLogger
from folker.model.entity import Action
from folker.model.error.load import InvalidSchemaDefinitionException
from folker.util.decorator import timed_action, resolvable_variables


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

    def validate(self):
        missing_fields = []

        if not hasattr(self, 'module') or not self.module:
            missing_fields.append('action.module')
        if not hasattr(self, 'method') or not self.method:
            missing_fields.append('action.method')

        if len(missing_fields) > 0:
            raise InvalidSchemaDefinitionException(missing_fields=missing_fields)

    @resolvable_variables
    @timed_action
    def execute(self, logger: TestLogger, test_context: dict, stage_context: dict) -> (dict, dict):
        module = __import__(self.module, fromlist=[self.method])
        method = getattr(module, self.method)
        result = method(**self.parameters)

        stage_context['result'] = result

        return test_context, stage_context

from folker.logger.logger import TestLogger
from folker.model.stage.action import Action
from folker.util.decorator import timed_action, resolvable_variables, loggable


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

    def mandatory_fields(self) -> [str]:
        return [
            'module',
            'method'
        ]

    @loggable
    @resolvable_variables
    @timed_action
    def execute(self, logger: TestLogger, test_context: dict, stage_context: dict) -> (dict, dict):
        module = __import__(self.module, fromlist=[self.method])
        method = getattr(module, self.method)
        result = method(**self.parameters)

        stage_context['result'] = result

        return test_context, stage_context

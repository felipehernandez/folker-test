from folker.decorator import timed_action, resolvable_variables, loggable_action
from folker.logger import TestLogger
from folker.model import Context
from folker.model import StageAction
from folker.module.void.action import VoidStageAction


class CodeStageAction(StageAction):
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
        self.parameters = parameters if parameters else {}

    def __add__(self, enrichment: 'CodeStageAction'):
        result = self.__copy__()
        if isinstance(enrichment, VoidStageAction):
            return result

        if enrichment.module:
            result.module = enrichment.module
        if enrichment.method:
            result.method = enrichment.method
        result.parameters = {**self.parameters, **enrichment.parameters}

        return result

    def mandatory_fields(self) -> [str]:
        return [
            'module',
            'method'
        ]

    @loggable_action
    @resolvable_variables
    @timed_action
    def execute(self, logger: TestLogger, context: Context) -> Context:
        module = __import__(self.module, fromlist=[self.method])
        method = getattr(module, self.method)
        result = method(**self.parameters)

        context.save_on_stage('result', result)

        return context

from folker.logger.logger import TestLogger
from folker.model.context import Context
from folker.model.stage import StageStep


class StageLog(StageStep):
    logs: set

    def __init__(self, logs: [str] = None) -> None:
        super().__init__()
        self.logs = set(logs) if logs else set()

    def __bool__(self):
        return True

    def __add__(self, enrichment: 'StageLog'):
        result = StageLog()

        result.logs = self.logs | enrichment.logs

        return result

    def execute(self, logger: TestLogger, context: Context) -> Context:
        for log in self.logs:
            logger.log_text(context.replace_variables(log))

        return context

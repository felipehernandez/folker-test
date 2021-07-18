from folker.logger.logger import TestLogger
from folker.model.context import Context
from folker.model.stage import StageStep


class StageLog(StageStep):
    logs: list

    def __init__(self, logs: [str] = None) -> None:
        super().__init__()
        self.logs = logs if logs else []

    def __bool__(self):
        return True

    def __add__(self, enrichment: 'StageLog'):
        result = StageLog()

        result.logs = [log for log in self.logs] + \
                      [log for log in enrichment.logs if log not in self.logs]

        return result

    def execute(self, logger: TestLogger, context: Context) -> Context:
        for log in self.logs:
            logger.log_text(context.replace_variables(log))

        return context

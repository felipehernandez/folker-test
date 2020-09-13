from folker.logger.logger import TestLogger
from folker.model.context import Context
from folker.model.stage import StageStep


class StageLog(StageStep):
    logs: [str]

    def __init__(self, logs: [str] = []) -> None:
        super().__init__()
        self.logs = logs if logs else []

    def enrich(self, template: 'StageLog'):
        new_data = []
        new_data.extend(self.logs + template.logs)
        self.logs = new_data

    def validate(self):
        pass

    def execute(self, logger: TestLogger, context: Context) -> Context:
        for log in self.logs:
            logger.log_text(context.replace_variables(log))

        return context

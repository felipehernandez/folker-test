from folker.logger.logger import TestLogger
from folker.model.stage.stage import StageStep
from folker.util.variable import replace_variables


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

    def execute(self, logger: TestLogger, test_context: dict, stage_context: dict) -> (dict, dict):
        for log in self.logs:
            logger.log_text(replace_variables(test_context, stage_context, log))

        return test_context, stage_context

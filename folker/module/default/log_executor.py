from folker import logger
from folker.model.data import StageData
from folker.model.task import LogExecutor
from folker.util.variable import replace_variables


class DefaultLogExecutor(LogExecutor):
    def execute(self, stage_data: StageData, test_context: dict, stage_context: dict) -> (dict, dict):
        for log in stage_data.log.logs:
            logger.log_text(replace_variables(test_context, stage_context, log))

        return test_context, stage_context

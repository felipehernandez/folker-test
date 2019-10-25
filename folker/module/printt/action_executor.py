import time

from folker import logger
from folker.model.data import StageData
from folker.model.task import ActionExecutor
from folker.util.variable import replace_variables


class PrintActionExecutor(ActionExecutor):

    def execute(self, stage_data: StageData, test_context: dict, stage_context: dict) -> (dict, dict):
        start = time.time()

        message = replace_variables(test_context, stage_context, stage_data.action.message)
        logger.message(message)

        end = time.time()
        stage_context['elapsed_time'] = int((end - start) * 1000)

        return test_context, stage_context

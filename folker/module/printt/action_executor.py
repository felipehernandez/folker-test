import time

from folker.model.task import ActionExecutor
from folker.module.printt.data import PrintStageData
from folker.util.variable import replace_variables


class PrintActionExecutor(ActionExecutor):

    def execute(self, stage_data: PrintStageData, test_context: dict, stage_context: dict) -> (dict, dict):
        start = time.time()

        message = replace_variables(test_context, stage_context, stage_data.action.message)
        self.logger.message(message)

        end = time.time()
        stage_context['elapsed_time'] = int((end - start) * 1000)

        return test_context, stage_context

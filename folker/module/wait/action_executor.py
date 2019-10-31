import time

from folker.model.task import ActionExecutor
from folker.module.wait.data import WaitStageData


class WaitActionExecutor(ActionExecutor):

    def execute(self, stage_data: WaitStageData, test_context: dict, stage_context: dict) -> (dict, dict):
        start = time.time()

        time.sleep(stage_data.action.time)

        end = time.time()
        stage_context['elapsed_time'] = int((end - start) * 1000)

        return test_context, stage_context

from folker.model.data import StageData
from folker.model.task import SaveExecutor
from folker.util.variable import replace_variables


class DefaultSaveExecutor(SaveExecutor):
    def execute(self, stage_data: StageData, test_context: dict, stage_context: dict) -> (dict, dict):
        for (variable, saving) in stage_data.save.save.items():
            test_context[variable] = replace_variables(test_context={}, stage_context=stage_context, text=saving)

        return test_context, stage_context

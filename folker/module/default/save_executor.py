from folker.model.data import StageData
from folker.model.task import SaveExecutor
from folker.util.variable import replace_variables, map_variables


class DefaultSaveExecutor(SaveExecutor):
    def execute(self, stage_data: StageData, test_context: dict, stage_context: dict) -> (dict, dict):
        for (variable, saving) in stage_data.save.save.items():
            try:
                updated_assertion, variables = map_variables(test_context, stage_context, saving)
                test_context[variable] = eval(updated_assertion)
            except Exception as e:
                test_context[variable] = replace_variables(test_context={}, stage_context=stage_context, text=saving)

        return test_context, stage_context

import collections
from copy import copy

from folker.logger.logger import TestLogger
from folker.model.stage.stage import StageStep
from folker.util.variable import replace_variables, map_variables


class StageSave(StageStep):
    save: dict

    def __init__(self, save: dict = {}) -> None:
        super().__init__()
        self.save = save if save else {}

    def __copy__(self):
        return copy(self)

    def enrich(self, template: 'StageSave'):
        new_data = {**self.save, **template.save}
        self.save = new_data

    def validate(self):
        pass

    def execute(self, logger: TestLogger, test_context: dict, stage_context: dict) -> (dict, dict):
        for (variable, saving) in self.save.items():
            variable = replace_variables(test_context, stage_context, variable)
            try:
                updated_saving, variables = map_variables(test_context, stage_context, saving)
                saving_value = eval(updated_saving, {'variables': variables})
            except Exception as e:
                saving_value = replace_variables(test_context=test_context, stage_context=stage_context, text=saving)

            test_context = self._resolve_variable(test_context, variable, saving_value)

        return test_context, stage_context

    def _resolve_variable(self, test_context: dict, variable, value) -> (str, object):
        variable_children = variable.split('.')

        if len(variable_children) == 1:
            test_context[variable] = value
            return test_context

        variable_root = variable_children[0]
        variable_value = {variable_children[-1]: value}
        path = variable_children[1:-1]
        for element in reversed(path):
            variable_value = {element: variable_value}

        test_context[variable_root] = self._merge_dictionaries(test_context.get(variable_root, {}), variable_value)
        return test_context

    def _merge_dictionaries(self, stable: dict, new_values: dict):
        if len(new_values) == 0:
            return stable
        for k, v in new_values.items():
            if (k in stable and isinstance(stable[k], dict)
                    and isinstance(new_values[k], collections.Mapping)):
                self._merge_dictionaries(stable[k], new_values[k])
            else:
                stable[k] = new_values[k]
        return stable

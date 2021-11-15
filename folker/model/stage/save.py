from copy import copy

from folker.logger import TestLogger
from folker.model.context import Context
from folker.model.stage import StageStep


class StageSave(StageStep):
    save: dict

    def __init__(self, save: dict = None) -> None:
        super().__init__()
        self.save = save if save else {}

    def __bool__(self):
        return True

    def __copy__(self):
        return copy(self)

    def __add__(self, enrichment: 'StageSave'):
        result = StageSave()

        result.save = {**self.save, **enrichment.save}

        return result

    def execute(self, logger: TestLogger, context: Context) -> Context:
        for (variable, saving) in self.save.items():
            variable = context.replace_variables(variable)
            try:
                updated_saving, variables = context.map_variables(saving)
                saving_value = eval(updated_saving, {'variables': variables})
            except Exception as e:
                saving_value = context.replace_variables(saving)

            context.save_on_test(variable, saving_value)

        return context

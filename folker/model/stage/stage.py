from copy import deepcopy

from folker.logger.logger import TestLogger
from folker.model.context import Context
from folker.model.error.error import SourceException
from folker.model.stage.assertions import StageAssertions
from folker.model.stage.log import StageLog
from folker.model.stage.save import StageSave
from folker.model.stage.stageaction import StageAction
from folker.model.validation import Validatable


class Stage(Validatable):
    id: str
    name: str

    condition: str
    foreach: dict

    action: StageAction

    save: StageSave
    log: StageLog
    assertions: StageAssertions

    def __init__(self,
                 id: str = None,
                 name: str = None,
                 condition: str = None,
                 foreach: dict = None,
                 action: StageAction = None,
                 log: [str] = None,
                 save: dict = None,
                 assertions: [str] = None,
                 **kwargs) -> None:
        super().__init__()
        self.id = id
        self.name = name

        self.condition = condition
        self.foreach = foreach if foreach else {}

        self.action = action
        self.save = StageSave(save)
        self.log = StageLog(log)
        self.assertions = StageAssertions(assertions)

    def __copy__(self):
        return deepcopy(self)

    def __add__(self, enrichment: 'Stage'):
        result = self.__copy__()

        if enrichment.name:
            result.name = enrichment.name
        if enrichment.condition:
            result.condition = enrichment.condition
        result.params = {**self.foreach, **enrichment.foreach}

        result.action = result.action + enrichment.action
        result.save = self.save + enrichment.save
        result.log = self.log + enrichment.log
        result.assertions = self.assertions + enrichment.assertions

        return result

    def __bool__(self):
        if not self.name and not self.id:
            self.validation_report.missing_fields.add('stage.name')
            self.validation_report.missing_fields.add('stage.id')

        if not self.action:
            self.validation_report.merge_with_prefix('stage[{name}].'.format(name=self.name),
                                                     self.action.validation_report)
        if not self.save:
            self.validation_report + self.save.validation_report
        if not self.log:
            self.validation_report + self.log.validation_report
        if not self.assertions:
            self.validation_report + self.assertions.validation_report

        return bool(self.validation_report)

    def execute(self, logger: TestLogger, context: Context):
        if self.skip_stage_execution(context):
            logger.stage_skip(context.replace_variables(self.name), context)
            return context

        contexts = context.replicate_on_stage(self.foreach)
        for stage_context in contexts:
            stage_context.test_variables = context.test_variables
            stage_context = self._execute(logger, stage_context)
            context.test_variables = stage_context.test_variables

        context.finalise_stage()
        return context

    def skip_stage_execution(self, context: Context):
        if self.condition is None:
            return False
        updated_assertion, variables = context.map_variables(self.condition)
        try:
            return not eval(updated_assertion, {'variables': variables})
        except Exception as e:
            return True

    def _execute(self, logger: TestLogger, context: Context):
        name = context.replace_variables(self.name)
        logger.stage_start(name, context)

        try:
            context = self.action.execute(logger=logger, context=context)
            context = self.save.execute(logger=logger, context=context)
            context = self.log.execute(logger=logger, context=context)
            context = self.assertions.execute(logger=logger, context=context)
        except SourceException as e:
            if not e.details:
                e.details = {}
            e.details['stage'] = self
            raise e

        return context

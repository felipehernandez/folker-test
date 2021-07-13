from copy import deepcopy

from folker.logger.logger import TestLogger
from folker.model.context import Context
from folker.model.error.error import SourceException
from folker.model.error.load import InvalidSchemaDefinitionException
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
                 foreach: dict = {},
                 action: StageAction = None,
                 log: [str] = None,
                 save: dict = None,
                 assertions: [str] = [],
                 **kwargs) -> None:
        super().__init__()
        self.id = id
        self.name = name

        self.condition = condition
        self.foreach = foreach

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

        enriched_action = enrichment.action.__copy__()
        enriched_action + self.action
        result.action = self.action + enrichment.action
        result.save = self.save + enrichment.save
        result.log = self.log + enrichment.log
        result.assertions = self.assertions + enrichment.assertions

        return result

    def __bool__(self):
        if not self.name and not self.id:
            self.validation_report.missing_fields.add('stage.name')
            self.validation_report.missing_fields.add('stage.id')

        if not self.action:
            self.validation_report + self.action.validation_report
        if not self.save:
            self.validation_report + self.save.validation_report
        if not self.log:
            self.validation_report + self.log.validation_report
        if not self.assertions:
            self.validation_report + self.assertions.validation_report

        return bool(self.validation_report)

    def enrich(self, template: 'Stage'):
        if self.name is None:
            self.name = template.name

        if self.condition is None:
            self.condition = template.condition
        if self.foreach != {}:
            new_data = {**self.foreach, **template.foreach}
            self.foreach = new_data

        if self.action:
            enriched_action = template.action.__copy__()
            enriched_action.enrich(self.action)
            self.action = enriched_action
        else:
            self.action = template.action.__copy__()
        if self.save:
            self.save.enrich(template.save)
        else:
            self.save = template.save.__copy__()
        if self.log:
            self.log.enrich(template.log)
        else:
            self.log = template.log.__copy__()
        if self.assertions:
            self.assertions.enrich(template.assertions)
        else:
            self.assertions = template.assertions.__copy__()

    def validate(self):
        if self.action is not None:
            self.action.validate()
        else:
            fields_message = '{}[name].action'.format(self.name) \
                if self.name \
                else '{}[id].action'.format(self.id)
            raise InvalidSchemaDefinitionException(wrong_fields=[fields_message])

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

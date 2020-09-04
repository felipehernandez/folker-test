from abc import ABC, abstractmethod

from folker.logger.logger import TestLogger
from folker.model.context import Context
from folker.model.error.error import SourceException
from folker.model.error.load import InvalidSchemaDefinitionException


# from folker.util.variable import build_contexts, replace_variables


class StageStep(ABC):
    @abstractmethod
    def execute(self, logger: TestLogger, test_context: dict, stage_context: dict) -> (dict, dict): pass

    @abstractmethod
    def enrich(self, template): pass

    @abstractmethod
    def validate(self): pass


from folker.model.stage.action import Action
from folker.model.stage.assertions import StageAssertions
from folker.model.stage.log import StageLog
from folker.model.stage.save import StageSave


class Stage:
    id: str
    name: str

    foreach: dict

    action: Action

    save: StageSave
    log: StageLog
    assertions: StageAssertions

    def __init__(self,
                 id: str = None,
                 name: str = None,
                 foreach: dict = {},
                 action: Action = None,
                 log: [str] = None,
                 save: dict = None,
                 assertions: [str] = [],
                 **kwargs) -> None:
        super().__init__()
        self.id = id
        self.name = name

        self.foreach = foreach

        self.action = action
        self.save = StageSave(save)
        self.log = StageLog(log)
        self.assertions = StageAssertions(assertions)

    def enrich(self, template: 'Stage'):
        if self.name is None:
            self.name = template.name

        if self.foreach != {}:
            new_data = {**self.foreach, **template.foreach}
            self.foreach = new_data

        if self.action:
            self.action.enrich(template.action)
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
            fields_message = '{}[name].action'.format(self.name) if self.name else '{}[id].action'.format(self.id)
            raise InvalidSchemaDefinitionException(wrong_fields=[fields_message])
        if self.save is not None:
            self.save.validate()
        if self.log is not None:
            self.log.validate()
        if self.assertions is not None:
            self.assertions.validate()

    def execute(self, logger: TestLogger, context: Context):
        contexts = context.replicate_on_stage(self.foreach)
        for stage_context in contexts:
            stage_context.test_variables = context.test_variables
            stage_context = self._execute(logger, stage_context)
            context.test_variables = stage_context.test_variables
        return context

    def _execute(self, logger: TestLogger, context: Context):
        name = context.replace_variables(self.name)
        logger.stage_start(name, context)

        try:
            context = self.action.execute(logger=logger, context=context)
            context = self.save.execute(logger=logger, context=context)
            context = self.log.execute(logger=logger, context=context)
            context = self.assertions.execute(logger=logger, context=context)
        except SourceException as e:
            e.details['stage'] = self
            raise e

        return context
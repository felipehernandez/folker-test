from abc import ABC, abstractmethod
from copy import deepcopy

from folker.logger.logger import TestLogger
from folker.model.context import Context
from folker.model.error.load import InvalidSchemaDefinitionException
from folker.model.stage.stage import StageStep


class Action(StageStep, ABC):
    def __copy__(self):
        return deepcopy(self)

    def enrich(self, template: 'Action'):
        for attribute, value in self.__dict__.items():
            self._set_attribute_if_missing(template, attribute)

    def _set_attribute_if_missing(self, template, attribute: str):
        if self.__getattribute__(attribute) is None:
            self.__setattr__(attribute, template.__getattribute__(attribute))

    @abstractmethod
    def mandatory_fields(self) -> [str]:
        pass

    def validate(self):
        missing_fields = []

        for attribute in self.mandatory_fields():
            if not hasattr(self, attribute) or not self.__getattribute__(attribute):
                missing_fields.append('action.' + attribute)

        missing_fields = self.validate_specific(missing_fields)

        if len(missing_fields) > 0:
            raise InvalidSchemaDefinitionException(missing_fields=missing_fields)

    def validate_specific(self, missing_fields):
        return missing_fields

    @abstractmethod
    def execute(self, logger: TestLogger, context: Context) -> Context:
        pass

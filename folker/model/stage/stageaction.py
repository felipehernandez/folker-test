from abc import abstractmethod, ABC
from copy import deepcopy

from folker.logger.logger import TestLogger
from folker.model.context import Context
from folker.model.stage import StageStep


class StageAction(StageStep, ABC):
    def __bool__(self):
        for attribute in self.mandatory_fields():
            if not hasattr(self, attribute) or not self.__getattribute__(attribute):
                self.validation_report.missing_fields.add('action.' + attribute)

        self._validate_specific()

        return bool(self.validation_report)

    def __copy__(self):
        return deepcopy(self)

    def _validate_specific(self):
        pass

    def _set_attribute_if_missing(self, template, attribute: str):
        if self.__getattribute__(attribute) is None \
                and hasattr(template, attribute):
            self.__setattr__(attribute, template.__getattribute__(attribute))

    @abstractmethod
    def mandatory_fields(self) -> [str]:
        pass

    @abstractmethod
    def execute(self, logger: TestLogger, context: Context) -> Context:
        pass

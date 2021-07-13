from abc import ABC, abstractmethod

from folker.logger.logger import TestLogger
from ..validation import Validatable


class StageStep(Validatable, ABC):
    @abstractmethod
    def execute(self, logger: TestLogger, test_context: dict, stage_context: dict) -> (dict, dict):
        pass

    @abstractmethod
    def enrich(self, template): pass

    @abstractmethod
    def validate(self): pass


from .stageaction import StageAction
from .assertions import StageAssertions
from .log import StageLog
from .save import StageSave
from .stage import Stage

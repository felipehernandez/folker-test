from abc import ABC, abstractmethod

from folker.logger.logger import TestLogger


class StageStep(ABC):
    @abstractmethod
    def execute(self, logger: TestLogger, test_context: dict, stage_context: dict) -> (dict, dict):
        pass

    @abstractmethod
    def enrich(self, template): pass

    @abstractmethod
    def validate(self): pass

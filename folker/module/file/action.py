import os
from enum import Enum, auto
from typing import List

from folker.decorator import timed_action, resolvable_variables, loggable_action
from folker.logger import TestLogger
from folker.model import Context
from folker.model import StageAction
from folker.module.void.action import VoidStageAction


class FileMethod(Enum):
    READ = auto()
    WRITE = auto()
    DELETE = auto()


class FileStageAction(StageAction):
    method: FileMethod = None
    file: str
    content: str

    def __init__(
        self, method: str = None, file: str = None, content: str = None, **kargs
    ) -> None:
        super().__init__()
        try:
            self.method = FileMethod[method]
        except Exception as ex:
            self.validation_report.wrong_fields.add("action.method")

        self.file = file
        self.content = content

    def __add__(self, enrichment: "FileStageAction"):
        result = self.__copy__()
        if isinstance(enrichment, VoidStageAction):
            return result

        if enrichment.file:
            result.file = enrichment.file
        if enrichment.content:
            result.content = enrichment.content

        return result

    def mandatory_fields(self) -> List[str]:
        return ["method", "file"]

    def _validate_specific(self):
        pass

    @loggable_action
    @resolvable_variables
    @timed_action
    def execute(self, logger: TestLogger, context: Context) -> Context:
       pass


class FileStageReadAction(FileStageAction):
    method: FileMethod = None
    file: str
    content: str

    def __init__(self, **fields):
        super().__init__(**fields)

    def _validate_specific(self):
        pass

    @loggable_action
    @resolvable_variables
    @timed_action
    def execute(self, logger: TestLogger, context: Context) -> Context:
        try:
            file = open(self.file, "r")
            context.save_on_stage("content", file.read())
            file.close()
        except Exception as e:
            logger.action_error(str(e))
            context.save_on_stage("error", e)

        return context


class FileStageWriteAction(FileStageAction):
    method: FileMethod = None
    file: str
    content: str

    def __init__(self, **fields):
        super().__init__(**fields)

    def _validate_specific(self):
        if not hasattr(self, "content") or not self.__getattribute__("content"):
            self.validation_report.missing_fields.add("action.content")

    @loggable_action
    @resolvable_variables
    @timed_action
    def execute(self, logger: TestLogger, context: Context) -> Context:
        try:
            file = open(self.file, "w")
            file.write(self.content)
            file.close()
        except Exception as e:
            logger.action_error(str(e))
            context.save_on_stage("error", e)

        return context


class FileStageDeleteAction(FileStageAction):
    method: FileMethod = None
    file: str
    content: str

    def __init__(self, **fields):
        super().__init__(**fields)

    def _validate_specific(self):
        pass

    @loggable_action
    @resolvable_variables
    @timed_action
    def execute(self, logger: TestLogger, context: Context) -> Context:
        try:
            if os.path.exists(self.file):
                os.remove(self.file)
            else:
                logger.action_warn(f"File {self.file} did not exists")
        except Exception as e:
            logger.action_error(str(e))
            context.save_on_stage("error", e)

        return context
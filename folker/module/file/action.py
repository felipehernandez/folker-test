import os
from enum import Enum, auto

from folker.logger.logger import TestLogger
from folker.model.entity import Action
from folker.model.error.load import InvalidSchemaDefinitionException
from folker.util.decorator import timed_action, resolvable_variables, loggable


class FileMethod(Enum):
    READ = auto()
    WRITE = auto()
    DELETE = auto()


class FileAction(Action):
    method: FileMethod
    file: str
    content: str

    def __init__(self,
                 method: str = None,
                 file: str = None,
                 content: str = None,
                 **kargs) -> None:
        super().__init__()
        if type:
            try:
                self.method = FileMethod[method]
            except:
                raise InvalidSchemaDefinitionException(wrong_fields=['action.method'])

        self.file = file
        self.content = content

    def mandatory_fields(self) -> [str]:
        return [
            'method',
            'file'
        ]

    def validate_specific(self, missing_fields):
        if FileMethod.WRITE == self.method and \
                (not hasattr(self, 'content') or not self.__getattribute__('content')):
            missing_fields.extend(['action.content'])

        return missing_fields

    @loggable
    @resolvable_variables
    @timed_action
    def execute(self, logger: TestLogger, test_context: dict, stage_context: dict) -> (dict, dict):
        {
            FileMethod.WRITE: self._write,
            FileMethod.READ: self._read,
            FileMethod.DELETE: self._delete,
        }[self.method](logger, test_context, stage_context)

        return test_context, stage_context

    def _write(self, logger: TestLogger, test_context: dict, stage_context: dict):
        try:
            file = open(self.file, 'w')
            file.write(self.content)
            file.close()
        except Exception as e:
            logger.action_error(str(e))
            stage_context['error'] = e

        return test_context, stage_context

    def _read(self, logger: TestLogger, test_context: dict, stage_context: dict):
        try:
            file = open(self.file, 'r')
            stage_context['content'] = file.read()
            file.close()
        except Exception as e:
            logger.action_error(str(e))
            stage_context['error'] = e

        return test_context, stage_context

    def _delete(self, logger: TestLogger, test_context: dict, stage_context: dict):
        try:
            if os.path.exists(self.file):
                os.remove(self.file)
            else:
                logger.action_warn("File {} did not exists".format(self.file))
        except Exception as e:
            logger.action_error(str(e))
            stage_context['error'] = e

        return test_context, stage_context
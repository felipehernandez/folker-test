from copy import copy, deepcopy

from folker.model.data import StageData, ActionData
from folker.model.error.load import InvalidSchemaDefinitionException


class PrintActionData(ActionData):
    message: str

    def __init__(self, message: str = None, template: bool = False, **kargs) -> None:
        super().__init__()

        if message:
            self.message = message

        if not template:
            self._validate_values()

    def __copy__(self):
        return deepcopy(self)

    def _validate_values(self):
        missing_fields = []

        if not hasattr(self, 'message') or not self.message:
            missing_fields.append('action.message')

        if len(missing_fields) > 0:
            raise InvalidSchemaDefinitionException(missing_fields=missing_fields)

    def enrich(self, message: str = None, **kargs):
        new_data = self.__copy__()

        if message:
            new_data.message = message

        new_data._validate_values()
        return new_data


class PrintStageData(StageData):
    action: PrintActionData

    def __init__(self, id=None, name=None, description=None, type=str, template: bool = False, **kargs) -> None:
        super().__init__(id, name, description, type, **kargs)

        if not template and 'action' not in kargs:
            raise InvalidSchemaDefinitionException(missing_fields=['action'])

        self.action = PrintActionData(**kargs['action'], template=template)

    def __copy__(self):
        return deepcopy(self)
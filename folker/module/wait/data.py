from copy import copy, deepcopy

from folker.model.data import StageData, ActionData
from folker.model.error.load import InvalidSchemaDefinitionException


class WaitActionData(ActionData):
    time: int

    def __init__(self, time=None, template: bool = False) -> None:
        super().__init__()

        if time:
            self.time = time

        if not template:
            self._validate_values()

    def __copy__(self):
        return copy(self)

    def _validate_values(self):
        missing_fields = []

        if not hasattr(self, 'time') or not self.time:
            missing_fields.append('action.time')

        if len(missing_fields) > 0:
            raise InvalidSchemaDefinitionException(missing_fields=missing_fields)

    def enrich(self, time=None, **kargs):
        new_data = self.__copy__()

        if time:
            new_data.time = time

        new_data._validate_values()
        return new_data

    def __copy__(self):
        return deepcopy(self)

class WaitStageData(StageData):
    action: WaitActionData

    def __init__(self, name: str, description: str = None, type: str = None, id=None, **kargs) -> None:
        super().__init__(id, name, description, type, **kargs)

        if 'action' not in kargs:
            raise InvalidSchemaDefinitionException(missing_fields=['action'])

        self.action = WaitActionData(**kargs['action'])

    def __copy__(self):
        return deepcopy(self)
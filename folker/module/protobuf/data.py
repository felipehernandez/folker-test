from copy import deepcopy
from enum import Enum, auto

from folker.model.data import ActionData, StageData
from folker.model.error.load import InvalidSchemaDefinitionException


class ProtobufMethod(Enum):
    LOAD = auto()
    CREATE = auto()


class ProtobufActionData(ActionData):
    method: ProtobufMethod
    package: str
    clazz: str

    def __init__(self,
                 method: str = None,
                 package: str = None,
                 clazz: str = None,
                 data=None,
                 message: str = None,
                 template: bool = False
                 ) -> None:
        super().__init__()

        if method:
            try:
                self.method = ProtobufMethod[method]
            except:
                self.method = None

        self.package = package
        self.clazz = clazz
        self.data = data
        self.message = message

        if not template:
            self._validate_values()

    def __copy__(self):
        return deepcopy(self)

    def _validate_values(self):
        missing_fields = []

        if not hasattr(self, 'method') or not self.method:
            missing_fields.append('action.method')
        if not hasattr(self, 'package') or not self.package:
            missing_fields.append('action.package')
        if not hasattr(self, 'clazz') or not self.clazz:
            missing_fields.append('action.class')
        if hasattr(self, 'method') and self.method == ProtobufMethod.WRITE and (not hasattr(self, 'data') or not self.data):
            missing_fields.append('action.data')
        if hasattr(self, 'method') and self.method == ProtobufMethod.LOAD and (not hasattr(self, 'message') or not self.message):
            missing_fields.append('action.message')

        if len(missing_fields) > 0:
            raise InvalidSchemaDefinitionException(missing_fields=missing_fields)

    def enrich(self,
               method: str = None,
               package: str = None,
               clazz: str = None,
               data=None,
               message: str = None
               ) -> None:
        new_data = self.__copy__()

        if method:
            try:
                new_data.method = ProtobufMethod[method]
            except:
                new_data.method = None
        new_data.package = package if package else None
        new_data.clazz = clazz if clazz else None
        new_data.data = data if data else None
        new_data.message = message if message else None

        new_data._validate_values()
        return new_data


class ProtobufStageData(StageData):
    action: ProtobufActionData

    def __init__(self, name: str = None, description: str = None, type: str = None, id: str = None, **kargs) -> None:
        super().__init__(id, name, description, type, **kargs)

        if 'action' not in kargs:
            raise InvalidSchemaDefinitionException(missing_fields=['action'])

        self.action = ProtobufActionData(**kargs['action'])

    def __copy__(self):
        return deepcopy(self)

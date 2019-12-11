from copy import deepcopy
from enum import Enum, auto

from folker.model.data import ActionData, StageData
from folker.model.error.load import InvalidSchemaDefinitionException


class RestMethod(Enum):
    GET = auto()
    POST = auto()
    PUT = auto()
    DELETE = auto()


class RestActionData(ActionData):
    method: RestMethod
    host: str
    uri: str
    params = dict()
    headers = dict()
    body = str
    body_json = str
    data = dict()

    def __init__(self,
                 method: str = None,
                 host: str = None,
                 uri: str = None,
                 params: dict = None,
                 headers: dict = None,
                 body=None,
                 data=None,
                 template: bool = False,
                 **kargs
                 ) -> None:
        super().__init__()

        if method:
            try:
                self.method = RestMethod[method]
            except:
                raise InvalidSchemaDefinitionException(wrong_fields=['action.method'])

        if host:
            self.host = host

        self.uri = uri
        self.query_parameters = params if params else {}
        self.headers = headers if headers else {}
        self.body = body
        self.body_json = kargs['json'] if kargs.__contains__('json') else None
        self.data = data
        self.params = params

        if not template:
            self._validate_values()

    def __copy__(self):
        return deepcopy(self)

    def _validate_values(self):
        missing_fields = []

        if not hasattr(self, 'method') or not self.method:
            missing_fields.append('action.method')
        if not hasattr(self, 'host') or not self.host:
            missing_fields.append('action.host')

        if len(missing_fields) > 0:
            raise InvalidSchemaDefinitionException(missing_fields=missing_fields)

    def enrich(self,
               method: str = None,
               host: str = None,
               uri: str = None,
               query_parameters: dict = None,
               headers: dict = None,
               body=None,
               **kargs):
        new_data = self.__copy__()

        if method:
            try:
                new_data.method = RestMethod[method]
            except:
                raise InvalidSchemaDefinitionException(wrong_fields=['action.method'])
        if host:
            new_data.host = host

        if uri:
            new_data.uri = uri
        if query_parameters:
            new_data.query_parameters = query_parameters if query_parameters else {}
        if headers:
            new_data.headers = headers if headers else {}
        if body:
            new_data.body = body
        if kargs.__contains__('json'):
            new_data.body_json = kargs['json'] if kargs.__contains__('json') else None

        new_data._validate_values()
        return new_data


class RestStageData(StageData):
    action: RestActionData

    def __init__(self, name: str = None, description: str = None, type: str = None, id: str = None, **kargs) -> None:
        super().__init__(id, name, description, type, **kargs)

        if 'action' not in kargs:
            raise InvalidSchemaDefinitionException(missing_fields=['action'])

        self.action = RestActionData(**kargs['action'])

    def __copy__(self):
        return deepcopy(self)

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
    query_parameters = dict()
    headers = dict()
    body = dict()
    body_json = str

    def __init__(self,
                 method: str = None,
                 host: str = None,
                 uri: str = None,
                 query_parameters: dict = None,
                 headers: dict = None,
                 body=None,
                 **kargs
                 ) -> None:
        super().__init__()
        missing_fields = []
        wrong_fields = []

        if method:
            try:
                self.method = RestMethod[method]
            except:
                wrong_fields.append('action.method')
        else:
            missing_fields.append('action.method')

        if host:
            self.host = host
        else:
            missing_fields.append('action.host')

        self.uri = uri
        self.query_parameters = query_parameters if query_parameters else {}
        self.headers = headers if headers else {}
        self.body = body
        self.body_json = kargs['json'] if kargs.__contains__('json') else None

        if len(missing_fields) > 0 or len(wrong_fields) > 0:
            raise InvalidSchemaDefinitionException(missing_fields=missing_fields, wrong_fields=wrong_fields)


class RestStageData(StageData):
    action: RestActionData

    def __init__(self, id, name, description=None, type=str, **kargs) -> None:
        super().__init__(id, name, description, type, **kargs)

        if 'action' not in kargs:
            raise InvalidSchemaDefinitionException(missing_fields=['action'])

        self.action = RestActionData(**kargs['action'])

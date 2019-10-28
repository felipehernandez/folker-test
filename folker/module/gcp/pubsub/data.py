from enum import Enum, auto

from folker.model.data import ActionData, StageData
from folker.model.error.load import InvalidSchemaDefinitionException


class PubSubMethod(Enum):
    PUBLISH = auto()
    SUBSCRIBE = auto()


class PubSubActionData(ActionData):
    method: PubSubMethod = None
    host: str
    uri: str
    query_parameters = dict()
    headers = dict()
    body = dict()
    body_json = str

    def __init__(self,
                 method: str = None,
                 project: str = None,
                 topic: str = None,
                 headers=None,
                 message=None,
                 subscription=None,
                 ack: bool = False,
                 **kargs
                 ) -> None:

        super().__init__()
        missing_fields = []
        wrong_fields = []

        if project:
            self.project = project
        else:
            missing_fields.append('action.project')

        if method:
            try:
                self.method = PubSubMethod[method]
            except:
                wrong_fields.append('action.method')
        else:
            missing_fields.append('action.method')

        if PubSubMethod.PUBLISH is self.method:
            if topic:
                self.topic = topic
            else:
                missing_fields.append('action.topic')

            if message:
                self.message = message
            else:
                missing_fields.append('action.message')

            self.headers = headers if headers else {}

        elif PubSubMethod.SUBSCRIBE is self.method:
            if subscription:
                self.subscription = subscription
            else:
                missing_fields.append('action.subscription')

            self.ack = ack

        if len(missing_fields) > 0 or len(wrong_fields) > 0:
            raise InvalidSchemaDefinitionException(missing_fields=missing_fields, wrong_fields=wrong_fields)


class PubSubStageData(StageData):
    action: PubSubActionData

    def __init__(self, id, name, description=None, type=str, **kargs) -> None:
        super().__init__(id, name, description, type, **kargs)

        if 'action' not in kargs:
            raise InvalidSchemaDefinitionException(missing_fields=['action'])

        self.action = PubSubActionData(**kargs['action'])

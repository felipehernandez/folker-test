from copy import deepcopy, copy
from enum import Enum, auto

from folker.model.data import ActionData, StageData
from folker.model.error.load import InvalidSchemaDefinitionException


class PubSubMethod(Enum):
    PUBLISH = auto()
    SUBSCRIBE = auto()


class PubSubActionData(ActionData):
    method: PubSubMethod = None
    project: str
    topic: str
    attributes: dict = {}
    message: str
    subscription: str
    ack: bool = False

    def __init__(self,
                 method: str = None,
                 project: str = None,
                 topic: str = None,
                 attributes: dict = None,
                 message=None,
                 subscription=None,
                 ack: bool = False,
                 template: bool = False,
                 **kargs
                 ) -> None:

        super().__init__()

        if project:
            self.project = project
        if method:
            try:
                self.method = PubSubMethod[method]
            except:
                raise InvalidSchemaDefinitionException(wrong_fields=['action.method'])
        if PubSubMethod.PUBLISH is self.method:
            if topic:
                self.topic = topic
            if message:
                self.message = message
            self.attributes = attributes if attributes else {}
        elif PubSubMethod.SUBSCRIBE is self.method:
            if subscription:
                self.subscription = subscription
            self.ack = ack

        if not template:
            self._validate_values()

    def __copy__(self):
        return copy(self)

    def _validate_values(self):
        missing_fields = []

        if not hasattr(self, 'project') or not self.project:
            missing_fields.append('action.project')
        if not hasattr(self, 'method') or not self.method:
            missing_fields.append('action.method')
        elif PubSubMethod.PUBLISH is self.method:
            missing_fields.extend(self._validate_publish_values())
        else:
            missing_fields.extend(self._validate_subscribe_values())

        if len(missing_fields) > 0:
            raise InvalidSchemaDefinitionException(missing_fields=missing_fields)

    def _validate_publish_values(self) -> [str]:
        missing_fields = []

        if not hasattr(self, 'topic') or not self.topic:
            missing_fields.append('action.topic')
        if not hasattr(self, 'message') or not self.message:
            missing_fields.append('action.message')

        return missing_fields

    def _validate_subscribe_values(self) -> [str]:
        missing_fields = []

        if not hasattr(self, 'subscription') or not self.subscription:
            missing_fields.append('action.subscription')

        return missing_fields

    def enrich(self,
               method: str = None,
               project: str = None,
               topic: str = None,
               attributes: dict = None,
               message=None,
               subscription=None,
               ack: bool = False,
               **kargs):
        new_data = self.__copy__()

        if method:
            try:
                new_data.method = PubSubMethod[method]
            except:
                raise InvalidSchemaDefinitionException(wrong_fields=['action.method'])
        if project:
            new_data.project = project
        if topic:
            new_data.topic = topic
        if attributes:
            new_data.attributes = attributes
        if message:
            new_data.message = message
        if subscription:
            new_data.subscription = subscription
        if ack:
            new_data.ack = ack

        new_data._validate_values()
        return new_data


class PubSubStageData(StageData):
    action: PubSubActionData

    def __init__(self, name: str = None, description: str = None, type: str = None, id: str = None, **kargs) -> None:
        super().__init__(id, name, description, type, **kargs)

        if 'action' not in kargs:
            raise InvalidSchemaDefinitionException(missing_fields=['action'])

        self.action = PubSubActionData(**kargs['action'])

    def __copy__(self):
        return deepcopy(self)

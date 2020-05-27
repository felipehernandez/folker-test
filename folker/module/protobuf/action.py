import json
from enum import Enum, auto

from google.protobuf import json_format
from google.protobuf.json_format import MessageToJson, MessageToDict

from folker.logger.logger import TestLogger
from folker.model.entity import Action
from folker.model.error.load import InvalidSchemaDefinitionException
from folker.util.decorator import timed_action, resolvable_variables


class ProtobufMethod(Enum):
    LOAD = auto()
    CREATE = auto()


class ProtobufAction(Action):
    method: ProtobufMethod
    package: str
    clazz: str
    data: dict
    message: str

    def __init__(self,
                 method: str = None,
                 package: str = None,
                 clazz: str = None,
                 data=None,
                 message: str = None,
                 **kargs) -> None:
        super().__init__()

        if method:
            try:
                self.method = ProtobufMethod[method]
            except:
                raise InvalidSchemaDefinitionException(wrong_fields=['action.method'])

        self.package = package + '_pb2' if package else None
        self.clazz = clazz
        self.data = data
        self.message = message

    def mandatory_fields(self) -> [str]:
        return [
            'method',
            'package'
        ]

    def validate_specific(self, missing_fields):
        if not hasattr(self, 'clazz') or not self.__getattribute__('clazz'):
            missing_fields.append('action.class')

        if hasattr(self, 'method') and self.method == ProtobufMethod.CREATE and (not hasattr(self, 'data') or not self.data):
            missing_fields.append('action.data')
        if hasattr(self, 'method') and self.method == ProtobufMethod.LOAD and (not hasattr(self, 'message') or not self.message):
            missing_fields.append('action.message')

        return missing_fields

    @resolvable_variables
    @timed_action
    def execute(self, logger: TestLogger, test_context: dict, stage_context: dict) -> (dict, dict):
        try:
            {
                ProtobufMethod.LOAD: self._load,
                ProtobufMethod.CREATE: self._create
            }[self.method](stage_context)

        except Exception as e:
            logger.action_error(str(e))
            stage_context['error'] = e

        return test_context, stage_context

    def _create(self, stage_context):
        mod = __import__(self.package, fromlist=[self.clazz])
        Proto = getattr(mod, self.clazz)
        parsed_object = json_format.Parse(json.dumps(self.data), Proto(), ignore_unknown_fields=False)

        stage_context['proto_object'] = parsed_object
        stage_context['proto_serialize'] = str(parsed_object.SerializeToString(), 'utf-8')

    def _load(self, stage_context):
        proto_package = self.package
        proto_class = self.clazz
        message = self.message

        mod = __import__(proto_package, fromlist=[proto_class])
        Proto = getattr(mod, proto_class)
        loaded_object = Proto()
        loaded_object.ParseFromString(message.encode())

        stage_context['proto_object'] = loaded_object
        stage_context['proto_json'] = MessageToJson(loaded_object)
        stage_context['proto_dict'] = MessageToDict(loaded_object)

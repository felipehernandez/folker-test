import json
import time
from copy import deepcopy
from enum import Enum, auto

from google.protobuf import json_format
from google.protobuf.json_format import MessageToJson, MessageToDict

from folker.logger.logger import TestLogger
from folker.model.entity import Action
from folker.model.error.load import InvalidSchemaDefinitionException
from folker.util.variable import recursive_replace_variables


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

        self.package = 'protos.' + package + '_pb2' if package else None
        self.clazz = clazz
        self.data = data
        self.message = message

    def __copy__(self):
        return deepcopy(self)

    def enrich(self, template: 'RestAction'):
        self._set_attribute_if_missing(template, 'method')
        self._set_attribute_if_missing(template, 'package')
        self._set_attribute_if_missing(template, 'clazz')
        self._set_attribute_if_missing(template, 'data')
        self._set_attribute_if_missing(template, 'message')

    def validate(self):
        missing_fields = []

        if not hasattr(self, 'method') or not self.method:
            missing_fields.append('action.method')
        if not hasattr(self, 'package') or not self.package:
            missing_fields.append('action.package')
        if not hasattr(self, 'clazz') or not self.clazz:
            missing_fields.append('action.class')
        if hasattr(self, 'method') and self.method == ProtobufMethod.CREATE and (not hasattr(self, 'data') or not self.data):
            missing_fields.append('action.data')
        if hasattr(self, 'method') and self.method == ProtobufMethod.LOAD and (not hasattr(self, 'message') or not self.message):
            missing_fields.append('action.message')

        if len(missing_fields) > 0:
            raise InvalidSchemaDefinitionException(missing_fields=missing_fields)

    def execute(self, logger: TestLogger, test_context: dict, stage_context: dict) -> (dict, dict):
        start = time.time()

        try:
            {
                ProtobufMethod.LOAD: self._load,
                ProtobufMethod.CREATE: self._create
            }[self.method](stage_context, test_context)

        except Exception as e:
            logger.action_error(str(e))
            stage_context['error'] = e

        end = time.time()
        stage_context['elapsed_time'] = int((end - start) * 1000)

        return test_context, stage_context

    def _create(self, stage_context, test_context):
        proto_package = recursive_replace_variables(test_context, stage_context, self.package)
        proto_class = recursive_replace_variables(test_context, stage_context, self.clazz)
        data = recursive_replace_variables(test_context, stage_context, self.data)

        mod = __import__(proto_package, fromlist=[proto_class])
        Proto = getattr(mod, proto_class)
        parsed_object = json_format.Parse(json.dumps(data), Proto(), ignore_unknown_fields=False)

        stage_context['proto_object'] = parsed_object
        stage_context['proto_serialize'] = str(parsed_object.SerializeToString(), 'utf-8')

    def _load(self, stage_context, test_context):
        proto_package = recursive_replace_variables(test_context, stage_context, self.package)
        proto_class = recursive_replace_variables(test_context, stage_context, self.clazz)
        message = recursive_replace_variables(test_context, stage_context, self.message)

        mod = __import__(proto_package, fromlist=[proto_class])
        Proto = getattr(mod, proto_class)
        loaded_object = Proto()
        loaded_object.ParseFromString(message.encode())

        stage_context['proto_object'] = loaded_object
        stage_context['proto_json'] = MessageToJson(loaded_object)
        stage_context['proto_dict'] = MessageToDict(loaded_object)

import json
import time

from google.protobuf import json_format
from google.protobuf.json_format import MessageToDict
from google.protobuf.json_format import MessageToJson

from folker.model.task import ActionExecutor
from folker.module.protobuf.data import ProtobufStageData, ProtobufActionData
from folker.util.variable import recursive_replace_variables


class ProtobufActionExecutor(ActionExecutor):

    def execute(self, stage_data: ProtobufStageData, test_context: dict, stage_context: dict) -> (dict, dict):
        start = time.time()

        try:
            protobuf_action = stage_data.action
            {
                'LOAD': self._load,
                'CREATE': self._create
            }[protobuf_action.method.name](protobuf_action, stage_context, test_context)

        except Exception as e:
            self.logger.action_error(str(e))
            stage_context['error'] = e

        end = time.time()
        stage_context['elapsed_time'] = int((end - start) * 1000)

        return test_context, stage_context

    def _create(self, protobuf_action: ProtobufActionData, stage_context, test_context):
        proto_package = recursive_replace_variables(test_context, stage_context, protobuf_action.package)
        proto_class = recursive_replace_variables(test_context, stage_context, protobuf_action.clazz)
        data = recursive_replace_variables(test_context, stage_context, protobuf_action.data)

        mod = __import__(proto_package, fromlist=[proto_class])
        Proto = getattr(mod, proto_class)
        parsed_object = json_format.Parse(json.dumps(data), Proto(), ignore_unknown_fields=False)

        stage_context['proto_object'] = parsed_object
        stage_context['proto_serialize'] = str(parsed_object.SerializeToString(), 'utf-8')

    def _load(self, protobuf_action, stage_context, test_context):
        proto_package = recursive_replace_variables(test_context, stage_context, protobuf_action.package)
        proto_class = recursive_replace_variables(test_context, stage_context, protobuf_action.clazz)
        message = recursive_replace_variables(test_context, stage_context, protobuf_action.message)

        mod = __import__(proto_package, fromlist=[proto_class])
        Proto = getattr(mod, proto_class)
        loaded_object = Proto()
        loaded_object.ParseFromString(message.encode())

        stage_context['proto_object'] = loaded_object
        stage_context['proto_json'] = MessageToJson(loaded_object)
        stage_context['proto_dict'] = MessageToDict(loaded_object)

import json
from enum import Enum, auto
from typing import List

from google.protobuf import json_format
from google.protobuf.json_format import MessageToJson, MessageToDict

from folker.decorator import timed_action, resolvable_variables, loggable_action
from folker.logger import TestLogger
from folker.model import Context
from folker.model import StageAction
from folker.model.error import InvalidSchemaDefinitionException
from folker.module.void.action import VoidStageAction


class ProtobufMethod(Enum):
    LOAD = auto()
    CREATE = auto()


class ProtobufStageAction(StageAction):
    method: ProtobufMethod
    package: str
    clazz: str
    data: dict
    message: str

    def __init__(
        self,
        method: str = None,
        package: str = None,
        clazz: str = None,
        data=None,
        message: str = None,
        **kargs
    ) -> None:
        super().__init__()

        if method:
            try:
                self.method = ProtobufMethod[method]
            except Exception as ex:
                raise InvalidSchemaDefinitionException(wrong_fields=["action.method"])

        self.package = package if package else None
        self.clazz = clazz
        self.data = data
        self.message = message

    def __add__(self, enrichment: "ProtobufStageAction"):
        result = self.__copy__()
        if isinstance(enrichment, VoidStageAction):
            return result

        if enrichment.package:
            result.package = enrichment.package
        if enrichment.clazz:
            result.clazz = enrichment.clazz
        if enrichment.data:
            result.data = enrichment.data
        if enrichment.message:
            result.message = enrichment.message

        return result

    def mandatory_fields(self) -> List[str]:
        return ["method", "package"]

    def _validate_specific(self):
        pass

    @loggable_action
    @resolvable_variables
    @timed_action
    def execute(self, logger: TestLogger, context: Context) -> Context:
        pass


class ProtobufStageLoadAction(ProtobufStageAction):
    method: ProtobufMethod
    package: str
    clazz: str
    data: dict
    message: str

    def __init__(self, **fields):
        super().__init__(**fields)

    def _validate_specific(self):
        if not hasattr(self, "clazz") or not self.__getattribute__("clazz"):
            self.validation_report.missing_fields.add("action.class")

        if not hasattr(self, "message") or not self.message:
            self.validation_report.missing_fields.add("action.message")

    @loggable_action
    @resolvable_variables
    @timed_action
    def execute(self, logger: TestLogger, context: Context) -> Context:
        try:
            self._load(context)
        except Exception as e:
            logger.action_error(str(e))
            context.save_on_stage("error", e)

        return context

    def _load(self, context: Context):
        proto_package = self.package + "_pb2"
        proto_class = self.clazz
        message = self.message

        mod = __import__(proto_package, fromlist=[proto_class])
        Proto = getattr(mod, proto_class)
        loaded_object = Proto()
        loaded_object.ParseFromString(message.encode())

        context.save_on_stage("proto_object", loaded_object)
        context.save_on_stage("proto_json", MessageToJson(loaded_object))
        context.save_on_stage("proto_dict", MessageToDict(loaded_object))


class ProtobufStageCreateAction(ProtobufStageAction):
    method: ProtobufMethod
    package: str
    clazz: str
    data: dict
    message: str

    def __init__(self, **fields):
        super().__init__(**fields)

    def _validate_specific(self):
        if not hasattr(self, "clazz") or not self.__getattribute__("clazz"):
            self.validation_report.missing_fields.add("action.class")

        if not hasattr(self, "data") or not self.data:
            self.validation_report.missing_fields.add("action.data")

    @loggable_action
    @resolvable_variables
    @timed_action
    def execute(self, logger: TestLogger, context: Context) -> Context:
        try:
            self._create(context)
        except Exception as e:
            logger.action_error(str(e))
            context.save_on_stage("error", e)

        return context

    def _create(self, context: Context):
        mod = __import__(self.package + "_pb2", fromlist=[self.clazz])
        Proto = getattr(mod, self.clazz)
        parsed_object = json_format.Parse(
            json.dumps(self.data), Proto(), ignore_unknown_fields=False
        )

        context.save_on_stage("proto_object", parsed_object)
        try:
            context.save_on_stage(
                "proto_serialize_str", parsed_object.SerializeToString()
            )
        except Exception as ex:
            context.save_on_stage("proto_serialize_str", "")
        try:
            context.save_on_stage(
                "proto_serialize_json",
                str(MessageToJson(parsed_object)).encode("utf-8"),
            )
        except Exception as ex:
            context.save_on_stage("proto_serialize_json", "")
        try:
            context.save_on_stage(
                "proto_serialize_utf8", str(parsed_object.SerializeToString(), "utf-8")
            )
        except Exception as ex:
            context.save_on_stage("proto_serialize_utf8", "")

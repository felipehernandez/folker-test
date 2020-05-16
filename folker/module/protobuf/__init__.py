from folker.load.schemas import ActionSchema
from folker.module.protobuf.schema import ProtobufActionSchema

ActionSchema.type_schemas['PROTOBUF'] = ProtobufActionSchema

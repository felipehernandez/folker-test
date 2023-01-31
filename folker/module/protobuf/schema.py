from marshmallow import Schema, fields, post_load

from folker.module.protobuf.action import ProtobufMethod, ProtobufStageAction, ProtobufStageCreateAction, ProtobufStageLoadAction


class ProtobufActionSchema(Schema):
    type = fields.String()

    method = fields.String()
    package = fields.String()
    clazz = fields.String(data_key='class')
    data = fields.Dict()
    message = fields.String()

    @post_load
    def make_action(self, data, **kwargs):
        return {
            ProtobufMethod.LOAD.name: ProtobufStageLoadAction,
            ProtobufMethod.CREATE.name: ProtobufStageCreateAction,
        }.get(data["method"], ProtobufStageAction)(**data)

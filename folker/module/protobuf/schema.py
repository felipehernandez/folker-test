from marshmallow import Schema, fields, post_load

from folker.module.protobuf.action import ProtobufStageAction


class ProtobufActionSchema(Schema):
    type = fields.String()

    method = fields.String()
    package = fields.String()
    clazz = fields.String(data_key='class')
    data = fields.Dict()
    message = fields.String()

    @post_load
    def make_action(self, data, **kwargs):
        return ProtobufStageAction(**data)

from marshmallow import Schema, fields, post_load

from folker.module.grpc.action import GrpcStageAction


class GrpcActionSchema(Schema):
    type = fields.String()

    host = fields.String()
    uri = fields.String()

    package = fields.String()
    stub = fields.String()
    method = fields.String()
    data = fields.String()

    @post_load
    def make_action(self, data, **kwargs):
        return GrpcStageAction(**data)

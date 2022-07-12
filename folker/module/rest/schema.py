from marshmallow import Schema, fields, post_load

from folker.module.rest.action import RestStageAction


class RestActionSchema(Schema):
    type = fields.String()

    method = fields.String()
    host = fields.String()
    uri = fields.String()
    params = fields.Dict(keys=fields.String(), values=fields.String())
    headers = fields.Dict(keys=fields.String(), values=fields.String())
    authorization = fields.Dict(keys=fields.String(), values=fields.String())
    body = fields.String()
    json = fields.Dict()
    data = fields.Dict()

    @post_load
    def make_action(self, data, **kwargs):
        return RestStageAction(**data)

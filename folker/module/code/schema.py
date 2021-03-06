from marshmallow import Schema, fields, post_load

from folker.module.code.action import CodeStageAction


class CodeActionSchema(Schema):
    type = fields.String()

    module = fields.String()
    method = fields.String()
    parameters = fields.Dict()

    @post_load
    def make_action(self, data, **kwargs):
        return CodeStageAction(**data)

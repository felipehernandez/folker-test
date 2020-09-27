from marshmallow import Schema, fields, post_load

from folker.module.printt.action import PrintStageAction


class PrintActionSchema(Schema):
    type = fields.String()

    message = fields.String()

    @post_load
    def make_action(self, data, **kwargs):
        return PrintStageAction(**data)

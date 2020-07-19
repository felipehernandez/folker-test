from marshmallow import Schema, fields, post_load

from folker.module.wait.action import WaitAction


class WaitActionSchema(Schema):
    type = fields.String()

    time = fields.Float()

    @post_load
    def make_action(self, data, **kwargs):
        return WaitAction(**data)

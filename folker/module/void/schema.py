from marshmallow import Schema, fields, post_load

from folker.module.void.action import VoidAction


class VoidActionSchema(Schema):
    type = fields.String()

    @post_load
    def make_action(self, data, **kwargs):
        return VoidAction(**data)

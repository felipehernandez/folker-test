from marshmallow import Schema, fields, post_load

from folker.module.file.action import FileAction


class FileActionSchema(Schema):
    type = fields.String()

    method = fields.String()
    file = fields.String()
    content = fields.String()

    @post_load
    def make_action(self, data, **kwargs):
        return FileAction(**data)

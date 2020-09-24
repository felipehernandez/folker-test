from marshmallow import Schema, fields, post_load

from folker.module.file.action import FileStageAction


class FileActionSchema(Schema):
    type = fields.String()

    method = fields.String()
    file = fields.String()
    content = fields.String()

    @post_load
    def make_action(self, data, **kwargs):
        return FileStageAction(**data)

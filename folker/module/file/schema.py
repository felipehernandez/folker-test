from marshmallow import Schema, fields, post_load

from folker.module.file.action import (
    FileMethod,
    FileStageAction,
    FileStageReadAction,
    FileStageWriteAction,
    FileStageDeleteAction,
)


class FileActionSchema(Schema):
    type = fields.String()

    method = fields.String()
    file = fields.String()
    content = fields.String()

    @post_load
    def make_action(self, data, **kwargs):
        return {
            FileMethod.READ.name: FileStageReadAction,
            FileMethod.WRITE.name: FileStageWriteAction,
            FileMethod.DELETE.name: FileStageDeleteAction,
        }.get(data["method"], FileStageAction)(**data)

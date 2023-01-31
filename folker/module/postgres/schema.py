from marshmallow import Schema, fields, post_load, pre_load

from folker.module.postgres.action import (
    PostgresMethod,
    PostgresStageAction,
    PostgresStageCreateAction,
    PostgresStageDeleteAction,
    PostgresStageDropAction,
    PostgresStageInsertAction,
    PostgresStageSelectAction,
    PostgresStageUpdateAction,
)


class PostgresActionSchema(Schema):
    type = fields.String()

    method = fields.String()
    host = fields.String()
    port = fields.String()
    user = fields.String()
    password = fields.String()
    database = fields.String()
    sql = fields.String()

    @pre_load
    def parse_port(self, in_data, **kwargs):
        if "port" not in in_data:
            return in_data
        in_data["port"] = str(in_data["port"])
        return in_data

    @post_load
    def make_action(self, data, **kwargs):
        return {
            PostgresMethod.CREATE.name: PostgresStageCreateAction,
            PostgresMethod.DELETE.name: PostgresStageDeleteAction,
            PostgresMethod.DROP.name: PostgresStageDropAction,
            PostgresMethod.INSERT.name: PostgresStageInsertAction,
            PostgresMethod.SELECT.name: PostgresStageSelectAction,
            PostgresMethod.UPDATE.name: PostgresStageUpdateAction,
        }.get(data["method"], PostgresStageAction)(**data)

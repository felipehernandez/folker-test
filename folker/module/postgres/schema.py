from marshmallow import Schema, fields, post_load, pre_load

from folker.module.postgres.action import PostgresStageAction


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
        if 'port' not in in_data:
            return in_data
        in_data['port'] = str(in_data['port'])
        return in_data

    @post_load
    def make_action(self, data, **kwargs):
        return PostgresStageAction(**data)

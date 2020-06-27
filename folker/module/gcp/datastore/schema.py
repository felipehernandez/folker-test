from marshmallow import Schema, fields, post_load

from folker.module.gcp.datastore.action import DatastoreAction


class DatastoreActionSchema(Schema):
    type = fields.String()

    method = fields.String()
    host = fields.String()
    project = fields.String()
    credentials = fields.String()

    key = fields.Dict()
    entity = fields.Dict()

    @post_load
    def make_action(self, data, **kwargs):
        return DatastoreAction(**data)

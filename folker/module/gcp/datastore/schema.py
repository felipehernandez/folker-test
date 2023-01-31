from marshmallow import Schema, fields, post_load

from folker.module.gcp.datastore.action import (
    DatastoreMethod,
    DatastoreStageAction,
    DatastoreStageBulkDeleteAction,
    DatastoreStageDeleteAction,
    DatastoreStageGetAction,
    DatastoreStagePutAction,
    DatastoreStageQueryAction,
)


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
        return {
            DatastoreMethod.PUT.name: DatastoreStagePutAction,
            DatastoreMethod.GET.name: DatastoreStageGetAction,
            DatastoreMethod.DELETE.name: DatastoreStageDeleteAction,
            DatastoreMethod.BULK_DELETE.name: DatastoreStageBulkDeleteAction,
            DatastoreMethod.QUERY.name: DatastoreStageQueryAction,
        }.get(data["method"], DatastoreStageAction)(**data)

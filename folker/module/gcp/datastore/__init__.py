from folker.load.schemas import ActionSchema
from folker.module.gcp.datastore.schema import DatastoreActionSchema

ActionSchema.type_schemas['DATASTORE'] = DatastoreActionSchema

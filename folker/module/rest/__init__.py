from folker.load.schemas import ActionSchema
from folker.module.rest.schema import RestActionSchema

ActionSchema.type_schemas['REST'] = RestActionSchema

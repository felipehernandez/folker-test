from folker.load.schemas import ActionSchema
from folker.module.void.schema import VoidActionSchema

ActionSchema.type_schemas['VOID'] = VoidActionSchema

from folker.load.schemas import ActionSchema
from folker.module.wait.schema import WaitActionSchema

ActionSchema.type_schemas['WAIT'] = WaitActionSchema

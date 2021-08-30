from folker.load.schemas import ActionSchema
from folker.module.printt.schema import PrintActionSchema

ActionSchema.type_schemas['PRINT'] = PrintActionSchema

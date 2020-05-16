from folker.load.schemas import ActionSchema
from folker.module.code.schema import CodeActionSchema

ActionSchema.type_schemas['CODE'] = CodeActionSchema

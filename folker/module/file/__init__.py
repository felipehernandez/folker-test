from folker.load.schemas import ActionSchema
from folker.module.file.schema import FileActionSchema

ActionSchema.type_schemas['FILE'] = FileActionSchema

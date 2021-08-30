from folker.load.schemas import ActionSchema
from folker.module.postgres.schema import PostgresActionSchema

ActionSchema.type_schemas['POSTGRES'] = PostgresActionSchema

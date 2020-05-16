from folker.load.schemas import ActionSchema
from folker.module.graphql.schema import GraphQLActionSchema

ActionSchema.type_schemas['GRAPHQL'] = GraphQLActionSchema

from marshmallow import Schema, fields, post_load

from folker.module.graphql.action import GraphQLStageAction


class GraphQLActionSchema(Schema):
    type = fields.String()

    host = fields.String()
    uri = fields.String()

    query = fields.String()
    mutation = fields.String()

    @post_load
    def make_action(self, data, **kwargs):
        return GraphQLStageAction(**data)

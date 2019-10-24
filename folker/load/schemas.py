from marshmallow import Schema, fields, post_load, pre_load

from folker import stage_builder
from folker.model.entity import Test


class ActionSchema(Schema):
    ack = fields.Boolean()
    host = fields.String()

    message = fields.String()
    method = fields.String()
    project = fields.String()
    subscription = fields.String()
    time = fields.Int()
    topic = fields.String()

    uri = fields.String()

    query_parameters = fields.Dict(keys=fields.String(), values=fields.String())
    headers = fields.Dict(keys=fields.String(), values=fields.String())
    body = fields.Dict()
    json = fields.Dict()


class StageSchema(Schema):
    id = fields.String(required=True)
    name = fields.String(required=True)
    type = fields.String(required=True)

    action = fields.Nested(ActionSchema)
    save = fields.Mapping()
    assertions = fields.List(cls_or_instance=fields.String, data_key='assert')
    log = fields.List(fields.String())

    @pre_load
    def parse_id(self, in_data, **kwargs):
        id_str_value = in_data['id']
        if str(id_str_value).isdigit():
            in_data['id'] = str(id_str_value)
        return in_data

    @post_load
    def make_test(self, data, **kwargs):
        stage = stage_builder.build(data)
        return stage


class TestSchema(Schema):
    test_name = fields.String(required=True)
    test_description = fields.String()
    stages = fields.Nested(StageSchema, required=True, many=True)

    @post_load
    def make_test(self, data, **kwargs):
        test = Test(**data)
        return test

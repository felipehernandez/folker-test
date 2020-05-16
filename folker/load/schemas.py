from marshmallow import Schema, fields, post_load, pre_load
from marshmallow_oneofschema import OneOfSchema

from folker.model.entity import Test, Stage


class ActionSchema(OneOfSchema):
    type_schemas = {}


class StageSchema(Schema):
    id = fields.String()
    name = fields.String()

    foreach = fields.Mapping()
    action = fields.Nested(ActionSchema)
    save = fields.Mapping()
    log = fields.List(fields.String())
    assertions = fields.List(cls_or_instance=fields.String, data_key='assert')

    @pre_load
    def parse_id(self, in_data, **kwargs):
        if 'id' not in in_data:
            return in_data
        id_str_value = in_data['id']
        if str(id_str_value).isdigit():
            in_data['id'] = str(id_str_value)
        return in_data

    @post_load
    def make_stage(self, data, **kwargs):
        stage = Stage(**data)
        return stage


class TestSchema(Schema):
    id = fields.String()
    name = fields.String()
    description = fields.String()
    parallel = fields.Boolean(default=False)

    foreach = fields.Mapping()
    tags = fields.List(fields.String())

    stages = fields.Nested(StageSchema, many=True)

    @post_load
    def make_test(self, data, **kwargs):
        test = Test(**data)
        return test

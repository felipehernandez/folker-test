from marshmallow import Schema, fields, post_load, pre_load

from folker import stage_builder
from folker.model.entity import Test, Template


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
    id = fields.String()
    name = fields.String()
    type = fields.String()

    action = fields.Nested(ActionSchema)
    save = fields.Mapping()
    assertions = fields.List(cls_or_instance=fields.String, data_key='assert')
    log = fields.List(fields.String())

    @pre_load
    def parse_id(self, in_data, **kwargs):
        if 'id' not in in_data:
            return in_data
        id_str_value = in_data['id']
        if str(id_str_value).isdigit():
            in_data['id'] = str(id_str_value)
        return in_data

    @post_load
    def make_test(self, data, **kwargs):
        stage = stage_builder.build_stage(data)
        return stage


class TemplatedStageSchema(StageSchema):
    @pre_load
    def parse_id(self, in_data, **kwargs):
        id_str_value = in_data['id']
        if str(id_str_value).isdigit():
            in_data['id'] = str(id_str_value)
        return in_data

    @post_load
    def make_test(self, data, **kwargs):
        stage = stage_builder.build_stage(data, template=True)
        return stage


class TestSchema(Schema):
    name = fields.String(required=True)
    description = fields.String()
    stages = fields.Nested(StageSchema, required=True, many=True)
    parallel = fields.Boolean(default=False)

    @post_load
    def make_test(self, data, **kwargs):
        test = Test(**data)
        return test


class TemplateSchema(Schema):
    id = fields.String(required=True)
    description = fields.String()
    stages = fields.Nested(TemplatedStageSchema, required=True, many=True)

    @post_load
    def make_test(self, data, **kwargs):
        test = Template(**data)
        return test

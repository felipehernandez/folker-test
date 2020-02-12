from marshmallow import Schema, fields, post_load, pre_load
from marshmallow_oneofschema import OneOfSchema

from folker.model.entity import Test, Stage
from folker.module.gcp.pubsub.action import PubSubAction
from folker.module.printt.action import PrintAction
from folker.module.protobuf.action import ProtobufAction
from folker.module.rest.action import RestAction
from folker.module.void.action import VoidAction
from folker.module.wait.action import WaitAction


class VoidActionSchema(Schema):
    type = fields.String()

    @post_load
    def make_action(self, data, **kwargs):
        return VoidAction(**data)


class PrintActionSchema(Schema):
    type = fields.String()

    message = fields.String()

    @post_load
    def make_action(self, data, **kwargs):
        return PrintAction(**data)


class WaitActionSchema(Schema):
    type = fields.String()

    time = fields.Float()

    @post_load
    def make_action(self, data, **kwargs):
        return WaitAction(**data)


class RestActionSchema(Schema):
    type = fields.String()

    method = fields.String()
    host = fields.String()
    uri = fields.String()
    params = fields.Dict(keys=fields.String(), values=fields.String())
    headers = fields.Dict(keys=fields.String(), values=fields.String())
    body = fields.String()
    json = fields.Dict()
    data = fields.Dict()

    @post_load
    def make_action(self, data, **kwargs):
        return RestAction(**data)


class ProtobufActionSchema(Schema):
    type = fields.String()

    method = fields.String()
    package = fields.String()
    clazz = fields.String(data_key='class')
    data = fields.Dict()
    message = fields.String()

    @post_load
    def make_action(self, data, **kwargs):
        return ProtobufAction(**data)


class PubSubActionSchema(Schema):
    type = fields.String()

    method = fields.String()
    project = fields.String()
    topic = fields.String()
    attributes = fields.Dict(keys=fields.String(), values=fields.String())
    message = fields.String()
    subscription = fields.String()
    ack = fields.Boolean()

    @post_load
    def make_action(self, data, **kwargs):
        return PubSubAction(**data)


class ActionSchema(OneOfSchema):
    type_schemas = {
        'VOID': VoidActionSchema,
        'PRINT': PrintActionSchema,
        'WAIT': WaitActionSchema,
        'REST': RestActionSchema,
        'PROTOBUF': ProtobufActionSchema,
        'PUBSUB': PubSubActionSchema
    }


class StageSchema(Schema):
    id = fields.String()
    name = fields.String()

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

    stages = fields.Nested(StageSchema, many=True)

    @post_load
    def make_test(self, data, **kwargs):
        test = Test(**data)
        return test

from marshmallow import Schema, fields, post_load, pre_load
from marshmallow_oneofschema import OneOfSchema

from folker.model import Profile
from folker.model import Test, Stage


class ActionSchema(OneOfSchema):
    type_schemas = {}


class StageSchema(Schema):
    id = fields.String()
    name = fields.String()
    description = fields.String()

    condition = fields.String(data_key='if')
    foreach = fields.Mapping()

    action = fields.Nested(ActionSchema)
    save = fields.Mapping()
    log = fields.List(fields.String())
    assertions = fields.List(cls_or_instance=fields.String, data_key='assert')

    @pre_load
    def pre_process_spec(self, in_data, **kwargs):
        if 'id' in in_data:
            id_str_value = in_data['id']
            if str(id_str_value).isdigit():
                in_data['id'] = str(id_str_value)

        return in_data

    @post_load
    def make_stage(self, data, **kwargs):
        # A stage that writes no action gets a VOID one; it is then either a reference to a
        # template stage or a stage that only saves, logs or asserts (BUG-22 tells them apart)
        declares_action = 'action' in data
        if not declares_action:
            # Imported here: every module package imports this file to register its schema
            from folker.module.void.action import VoidStageAction
            data['action'] = VoidStageAction()
        stage = Stage(**data)
        stage.declares_action = declares_action
        return stage


class TestSchema(Schema):
    id = fields.String()
    name = fields.String()
    description = fields.String()
    parallel = fields.Boolean(dump_default=False)

    foreach = fields.Mapping()
    tags = fields.List(fields.String())

    stages = fields.Nested(StageSchema, many=True)

    @post_load
    def make_test(self, data, **kwargs):
        test = Test(**data)
        return test


class ProfileSchema(Schema):
    name = fields.String()
    context = fields.Mapping()
    secrets = fields.Mapping()

    @post_load
    def make_profile(self, data, **kwargs):
        profile = Profile(**data)
        return profile

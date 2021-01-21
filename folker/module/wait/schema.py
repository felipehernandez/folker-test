from marshmallow import Schema, fields, post_load, pre_load

from folker.module.wait.action import WaitStageAction


class WaitActionSchema(Schema):
    type = fields.String()

    time = fields.String(strict=False)

    @pre_load
    def pre_process_spec(self, in_data, **kwargs):
        if 'time' not in in_data:
            return in_data
        in_data['time'] = str(in_data['time'])
        return in_data

    @post_load
    def make_action(self, data, **kwargs):
        return WaitStageAction(**data)

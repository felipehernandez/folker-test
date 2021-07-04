from marshmallow import Schema, fields, post_load

from folker.module.zookeeper.action import ZookeeperStageAction


class ZookeeperActionSchema(Schema):
    type = fields.String()

    host = fields.String()
    method = fields.String()
    node = fields.String()
    data = fields.String()
    ephemeral = fields.Boolean()

    @post_load
    def make_action(self, data, **kwargs):
        return ZookeeperStageAction(**data)

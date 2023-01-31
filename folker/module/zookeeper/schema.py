from marshmallow import Schema, fields, post_load

from folker.module.zookeeper.action import (
    ZookeeperMethod,
    ZookeeperStageAction,
    ZookeeperStageExistsAction,
    ZookeeperStageCreateAction,
    ZookeeperStageDeleteAction,
    ZookeeperStageGetAction,
    ZookeeperStageSetAction,
)


class ZookeeperActionSchema(Schema):
    type = fields.String()

    host = fields.String()
    method = fields.String()
    node = fields.String()
    data = fields.String()
    ephemeral = fields.Boolean()

    @post_load
    def make_action(self, data, **kwargs):
        return {
            ZookeeperMethod.EXISTS.name: ZookeeperStageExistsAction,
            ZookeeperMethod.CREATE.name: ZookeeperStageCreateAction,
            ZookeeperMethod.DELETE.name: ZookeeperStageDeleteAction,
            ZookeeperMethod.GET.name: ZookeeperStageGetAction,
            ZookeeperMethod.SET.name: ZookeeperStageSetAction,
        }.get(data["method"], ZookeeperStageAction)(**data)

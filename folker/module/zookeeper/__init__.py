from folker.load.schemas import ActionSchema
from folker.module.zookeeper.schema import ZookeeperActionSchema

ActionSchema.type_schemas['ZOOKEEPER'] = ZookeeperActionSchema

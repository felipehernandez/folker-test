from folker.load.schemas import ActionSchema
from folker.module.rabbitmq.schema import RabbitMQActionSchema

ActionSchema.type_schemas['RABBITMQ'] = RabbitMQActionSchema

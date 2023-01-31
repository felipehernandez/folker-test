from marshmallow import Schema, fields, post_load

from folker.module.rabbitmq.action import (
    RabbitMQMethod,
    RabbitMQStageAction,
    RabbitMQStageClearAction,
    RabbitMQStageCountAction,
    RabbitMQStagePublishAction,
    RabbitMQStageSubscribeAction,
)


class RabbitMQActionSchema(Schema):
    type = fields.String()

    method = fields.String()
    host = fields.String()
    port = fields.String()
    vhost = fields.String()

    user = fields.String()
    password = fields.String()

    exchange = fields.String()
    message = fields.String()

    queue = fields.String()
    ack = fields.Boolean()

    @post_load
    def make_action(self, data, **kwargs):
        return {
            RabbitMQMethod.PUBLISH.name: RabbitMQStagePublishAction,
            RabbitMQMethod.SUBSCRIBE.name: RabbitMQStageSubscribeAction,
            RabbitMQMethod.COUNT.name: RabbitMQStageCountAction,
            RabbitMQMethod.CLEAR.name: RabbitMQStageClearAction,
        }.get(data["method"], RabbitMQStageAction)(**data)
        return RabbitMQStageAction(**data)

from marshmallow import Schema, fields, post_load

from folker.module.kafka.action import (
    KafkaMethod,
    KafkaStageAction,
    KafkaStagePublishAction,
    KafkaStageSubscribeAction,
)


class KafkaActionSchema(Schema):
    type = fields.String()
    method = fields.String()

    host = fields.String()
    topic = fields.String()

    key = fields.String()
    message = fields.String()
    headers = fields.Dict(keys=fields.String(), values=fields.String())
    group = fields.String()

    @post_load
    def make_action(self, data, **kwargs):
        return {
            KafkaMethod.PUBLISH.name: KafkaStagePublishAction,
            KafkaMethod.SUBSCRIBE.name: KafkaStageSubscribeAction,
        }.get(data["method"], KafkaStageAction)(**data)

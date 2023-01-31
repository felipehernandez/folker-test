from marshmallow import Schema, fields, post_load

from folker.module.gcp.pubsub.action import (
    PubSubMethod,
    PubSubStageAction,
    PubSubStagePublishAction,
    PubSubStageSubscribeAction,
    PubSubStageSubscriptionsAction,
    PubSubStageTopicsAction,
)


class PubSubActionSchema(Schema):
    type = fields.String()

    method = fields.String()
    host = fields.String()
    project = fields.String()
    credentials = fields.String()

    topic = fields.String()
    attributes = fields.Dict(keys=fields.String(), values=fields.String())
    message = fields.String()
    subscription = fields.String()
    ack = fields.Boolean()

    @post_load
    def make_action(self, data, **kwargs):
        return {
            PubSubMethod.PUBLISH.name: PubSubStagePublishAction,
            PubSubMethod.SUBSCRIBE.name: PubSubStageSubscribeAction,
            PubSubMethod.TOPICS.name: PubSubStageTopicsAction,
            PubSubMethod.SUBSCRIPTIONS.name: PubSubStageSubscriptionsAction,
        }.get(data["method"], PubSubStageAction)(**data)

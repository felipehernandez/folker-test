import json
import os
from copy import deepcopy
from enum import Enum, auto

import grpc
from google.cloud.pubsub_v1 import PublisherClient, SubscriberClient
from google.cloud.pubsub_v1.proto.pubsub_pb2 import PubsubMessage

from folker.logger.logger import TestLogger
from folker.model.entity import Action
from folker.model.error.load import InvalidSchemaDefinitionException
from folker.util.decorator import timed_action, resolvable_variables, loggable


class PubSubMethod(Enum):
    PUBLISH = auto()
    SUBSCRIBE = auto()
    TOPICS = auto()
    SUBSCRIPTIONS = auto()


class PubSubAction(Action):
    method: PubSubMethod
    host: str
    project: str
    topic: str
    attributes: dict = {}
    message: str
    subscription: str
    ack: bool = False

    def __init__(self,
                 method: str = None,
                 host: str = None,
                 project: str = None,
                 topic: str = None,
                 subscription=None,
                 attributes: dict = None,
                 message=None,
                 ack: bool = False,
                 **kargs) -> None:
        super().__init__()

        if method:
            try:
                self.method = PubSubMethod[method]
            except:
                raise InvalidSchemaDefinitionException(wrong_fields=['action.method'])

        self.host = host
        self.project = project
        self.attributes = attributes

        self.topic = topic
        self.message = message

        self.subscription = subscription
        self.ack = ack

    def __copy__(self):
        return deepcopy(self)

    def mandatory_fields(self):
        return [
            'project',
            'method'
        ]

    def validate_specific(self, missing_fields):
        if hasattr(self, 'method') and PubSubMethod.PUBLISH is self.method:
            missing_fields.extend(self._validate_publish_values())
        if hasattr(self, 'method') and PubSubMethod.SUBSCRIBE is self.method:
            missing_fields.extend(self._validate_subscribe_values())

        return missing_fields

    def _validate_publish_values(self) -> [str]:
        missing_fields = []

        if not hasattr(self, 'topic') or not self.topic:
            missing_fields.append('action.topic')
        if not hasattr(self, 'message') or not self.message:
            missing_fields.append('action.message')

        return missing_fields

    def _validate_subscribe_values(self) -> [str]:
        missing_fields = []

        if not hasattr(self, 'subscription') or not self.subscription:
            missing_fields.append('action.subscription')

        return missing_fields

    @loggable
    @resolvable_variables
    @timed_action
    def execute(self, logger: TestLogger, test_context: dict, stage_context: dict) -> (dict, dict):
        {
            PubSubMethod.PUBLISH: self._publish,
            PubSubMethod.SUBSCRIBE: self._subscribe,
            PubSubMethod.TOPICS: self._topics,
            PubSubMethod.SUBSCRIPTIONS: self._subscriptions
        }.get(self.method)(logger, stage_context)

        return test_context, stage_context

    def _publish(self, logger: TestLogger, stage_context: dict):
        self._authenticate()

        self.publisher = PublisherClient(channel=grpc.insecure_channel(target=self.host)) if self.host else PublisherClient()

        topic_path = self.publisher.topic_path(self.project, self.topic)
        attributes = self.attributes if self.attributes else {}

        self._log_debug(logger, topic=topic_path, attributes=attributes, message=self.message)
        future = self.publisher.publish(topic=topic_path, data=self.message.encode(), **attributes)

        stage_context['message_id'] = future.result()

    def _subscribe(self, logger: TestLogger, stage_context: dict):
        self._authenticate()

        self.subscriber = SubscriberClient(channel=grpc.insecure_channel(target=self.host)) if self.host else SubscriberClient()

        subscription_path = self.subscriber.subscription_path(self.project, self.subscription)

        self._log_debug(logger, subscription=subscription_path, ack=self.ack)
        response = self.subscriber.pull(subscription=subscription_path, max_messages=1)

        for message in response.received_messages:
            message: PubsubMessage
            stage_context['ack_id'] = message.ack_id
            stage_context['message_id'] = message.message.message_id
            stage_context['publish_time'] = message.message.publish_time
            stage_context['attributes'] = message.message.attributes
            stage_context['message_content'] = message.message.data.decode('UTF-8')

            if self.ack:
                self.subscriber.acknowledge(subscription_path, [message.ack_id])

    def _topics(self, logger: TestLogger, stage_context: dict):
        self._authenticate()

        self.publisher = PublisherClient(channel=grpc.insecure_channel(target=self.host)) if self.host else PublisherClient()

        project_path = self.publisher.project_path(self.project)
        topics = self.publisher.list_topics(project_path)

        topic_prefix = project_path + '/topics/'
        prefix_len = len(topic_prefix)
        stage_context['topics'] = [topic.name[prefix_len:] for topic in topics]

    def _subscriptions(self, logger: TestLogger, stage_context: dict):
        self._authenticate()

        self.subscriber = SubscriberClient(channel=grpc.insecure_channel(target=self.host)) if self.host else SubscriberClient()

        project = self.project
        project_path = self.subscriber.project_path(project)
        subscriptions = self.subscriber.list_subscriptions(project_path)

        subscription_prefix = project_path + '/subscriptions/'
        stage_context['subscriptions'] = [subscription.name[len(subscription_prefix):] for subscription in subscriptions]

    def _authenticate(self):
        credentials_path = os.getcwd() + '/credentials/gcp/gcp-credentials.json'
        if os.path.exists(credentials_path):
            self.credentials_path = credentials_path
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.credentials_path

    @staticmethod
    def _log_debug(logger: TestLogger, **parameters):
        logger.action_debug(json.dumps(parameters))

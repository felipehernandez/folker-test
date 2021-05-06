import json
import os
from copy import deepcopy
from enum import Enum, auto

import grpc
from google.cloud.pubsub import PublisherClient, SubscriberClient

from folker.decorator import timed_action, resolvable_variables, loggable_action
from folker.logger import TestLogger
from folker.model import Context
from folker.model import StageAction
from folker.model.error import InvalidSchemaDefinitionException


class PubSubMethod(Enum):
    PUBLISH = auto()
    SUBSCRIBE = auto()
    TOPICS = auto()
    SUBSCRIPTIONS = auto()


class PubSubStageAction(StageAction):
    method: PubSubMethod

    host: str
    project: str
    credentials_path: str

    topic: str
    attributes: dict = {}
    message: str
    subscription: str
    ack: bool = False

    def __init__(self,
                 method: str = None,
                 host: str = None,
                 project: str = None,
                 credentials: str = None,
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
        self.credentials_path = credentials

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

    @loggable_action
    @resolvable_variables
    @timed_action
    def execute(self, logger: TestLogger, context: Context) -> Context:
        self._authenticate()
        {
            PubSubMethod.PUBLISH: self._publish,
            PubSubMethod.SUBSCRIBE: self._subscribe,
            PubSubMethod.TOPICS: self._topics,
            PubSubMethod.SUBSCRIPTIONS: self._subscriptions
        }.get(self.method)(logger, context)

        return context

    def _publish(self, logger: TestLogger, context: Context):
        self.publisher = PublisherClient(channel=grpc.insecure_channel(target=self.host)) \
            if self.host \
            else PublisherClient()

        topic_path = self.publisher.topic_path(self.project, self.topic)
        attributes = self.attributes if self.attributes else {}

        self._log_debug(logger, topic=topic_path, attributes=attributes, message=str(self.message))
        future = self.publisher.publish(topic=topic_path, data=self.message, **attributes)

        context.save_on_stage('message_id', future.result())

    def _subscribe(self, logger: TestLogger, context: Context):
        self.subscriber = SubscriberClient(channel=grpc.insecure_channel(target=self.host)) \
            if self.host \
            else SubscriberClient()

        subscription_path = self.subscriber.subscription_path(self.project, self.subscription)

        self._log_debug(logger, subscription=subscription_path, ack=self.ack)
        response = self.subscriber.pull(request={"subscription": subscription_path,
                                                 "max_messages": 1})

        for message in response.received_messages:
            context.save_on_stage('ack_id', message.ack_id)
            context.save_on_stage('message_id', message.message.message_id)
            context.save_on_stage('publish_time', message.message.publish_time)
            context.save_on_stage('attributes', message.message.attributes)
            context.save_on_stage('message_content', message.message.data.decode('UTF-8'))

            if self.ack:
                self.subscriber.acknowledge(request={"subscription": subscription_path,
                                                     "ack_ids": [message.ack_id]})

    def _topics(self, logger: TestLogger, context: Context):
        self.publisher = PublisherClient(channel=grpc.insecure_channel(target=self.host)) \
            if self.host \
            else PublisherClient()

        project_path = 'projects/{project_id}'.format(project_id=self.project)
        topics = self.publisher.list_topics(project=project_path)

        topic_prefix = project_path + '/topics/'
        prefix_len = len(topic_prefix)
        context.save_on_stage('topics', [topic.name[prefix_len:] for topic in topics])

    def _subscriptions(self, logger: TestLogger, context: Context):
        self.subscriber = SubscriberClient(channel=grpc.insecure_channel(target=self.host)) \
            if self.host \
            else SubscriberClient()

        project_path = 'projects/{project_id}'.format(project_id=self.project)
        subscriptions = self.subscriber.list_subscriptions(project=project_path)

        subscription_prefix = project_path + '/subscriptions/'
        context.save_on_stage('subscriptions',
                              [subscription.name[len(subscription_prefix):]
                               for subscription in subscriptions])

    def _authenticate(self):
        credentials_path = os.getcwd() + '/credentials/gcp/gcp-credentials.json'
        if os.path.exists(credentials_path):
            self.credentials_path = credentials_path
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.credentials_path

    @staticmethod
    def _log_debug(logger: TestLogger, **parameters):
        logger.action_debug(json.dumps(parameters))

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
from folker.module.void.action import VoidStageAction


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
    attributes: dict
    message: str
    subscription: str
    ack: bool = None

    def __init__(self,
                 method: str = None,
                 host: str = None,
                 project: str = None,
                 credentials: str = None,
                 topic: str = None,
                 subscription=None,
                 attributes: dict = None,
                 message=None,
                 ack: bool = None,
                 **kargs) -> None:
        super().__init__()

        if method:
            try:
                self.method = PubSubMethod[method]
            except Exception as ex:
                raise InvalidSchemaDefinitionException(wrong_fields=['action.method'])

        self.host = host
        self.project = project
        self.credentials_path = credentials

        self.attributes = attributes if attributes else {}

        self.topic = topic
        self.message = message

        self.subscription = subscription
        self.ack = ack

    def __copy__(self):
        return deepcopy(self)

    def __add__(self, enrichment: 'PubSubStageAction'):
        result = self.__copy__()
        if isinstance(enrichment, VoidStageAction):
            return result

        if enrichment.host:
            result.host = enrichment.host
        if enrichment.project:
            result.project = enrichment.project
        if enrichment.credentials_path:
            result.credentials_path = enrichment.credentials_path
        if enrichment.topic:
            result.topic = enrichment.topic
        if enrichment.message:
            result.message = enrichment.message
        if enrichment.subscription:
            result.subscription = enrichment.subscription
        if enrichment.ack:
            result.ack = enrichment.ack
        result.attributes = {**self.attributes, **enrichment.attributes}

        return result

    def mandatory_fields(self):
        return [
            'project',
            'method'
        ]

    def _validate_specific(self):
        if hasattr(self, 'method') and PubSubMethod.PUBLISH is self.method:
            if not hasattr(self, 'topic') or not self.topic:
                self.validation_report.missing_fields.add('action.topic')
            if not hasattr(self, 'message') or not self.message:
                self.validation_report.missing_fields.add('action.message')
        if hasattr(self, 'method') and PubSubMethod.SUBSCRIBE is self.method:
            if not hasattr(self, 'subscription') or not self.subscription:
                self.validation_report.missing_fields.add('action.subscription')

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

        message = self.message \
            if isinstance(self.message, (bytes, bytearray)) \
            else self.message.encode()
        future = self.publisher.publish(topic=topic_path, data=message, **attributes)

        context.save_on_stage('message_id', future.result())

    def _subscribe(self, logger: TestLogger, context: Context):
        self.subscriber = SubscriberClient(channel=grpc.insecure_channel(target=self.host)) \
            if self.host \
            else SubscriberClient()

        subscription_path = self.subscriber.subscription_path(self.project, self.subscription)

        self._log_debug(logger, subscription=subscription_path, ack=bool(self.ack))
        response = self.subscriber.pull(subscription=subscription_path,
                                        max_messages=1)

        for message in response.received_messages:
            context.save_on_stage('ack_id', message.ack_id)
            context.save_on_stage('message_id', message.message.message_id)
            context.save_on_stage('publish_time', message.message.publish_time)
            context.save_on_stage('attributes', message.message.attributes)
            context.save_on_stage('message_content', message.message.data.decode('UTF-8'))

            if self.ack:
                self.subscriber.acknowledge(subscription=subscription_path,
                                            ack_ids=[message.ack_id])

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

import json
import os
import time
from copy import deepcopy
from enum import Enum, auto

from google.cloud.pubsub_v1 import PublisherClient, SubscriberClient
from google.cloud.pubsub_v1.proto.pubsub_pb2 import PubsubMessage

from folker.logger.logger import TestLogger
from folker.model.entity import Action
from folker.model.error.load import InvalidSchemaDefinitionException
from folker.util.variable import recursive_replace_variables


class PubSubMethod(Enum):
    PUBLISH = auto()
    SUBSCRIBE = auto()


class PubSubAction(Action):
    method: PubSubMethod
    project: str
    topic: str
    attributes: dict = {}
    message: str
    subscription: str
    ack: bool = False

    def __init__(self,
                 method: str = None,
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

        self.project = project
        self.attributes = attributes

        self.topic = topic
        self.message = message

        self.subscription = subscription
        self.ack = ack

    def __copy__(self):
        return deepcopy(self)

    def enrich(self, template: 'ProtobufAction'):
        self._set_attribute_if_missing(template, 'method')
        self._set_attribute_if_missing(template, 'project')
        self._set_attribute_if_missing(template, 'topic')
        self._set_attribute_if_missing(template, 'subscription')
        self._set_attribute_if_missing(template, 'attributes')
        self._set_attribute_if_missing(template, 'message')
        self._set_attribute_if_missing(template, 'ack')

    def validate(self):
        missing_fields = []

        if not hasattr(self, 'project') or not self.project:
            missing_fields.append('action.project')
        if not hasattr(self, 'method') or not self.method:
            missing_fields.append('action.method')
        elif PubSubMethod.PUBLISH is self.method:
            missing_fields.extend(self._validate_publish_values())
        else:
            missing_fields.extend(self._validate_subscribe_values())

        if len(missing_fields) > 0:
            raise InvalidSchemaDefinitionException(missing_fields=missing_fields)

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

    def execute(self, logger: TestLogger, test_context: dict, stage_context: dict) -> (dict, dict):
        start = time.time()

        {
            PubSubMethod.PUBLISH: self._publish,
            PubSubMethod.SUBSCRIBE: self._subscribe
        }.get(self.method)(logger, test_context, stage_context)

        end = time.time()
        stage_context['elapsed_time'] = int((end - start) * 1000)

        return test_context, stage_context

    def _publish(self, logger: TestLogger, test_context: dict, stage_context: dict):
        self._authenticate()

        self.publisher = PublisherClient()

        project = recursive_replace_variables(test_context, stage_context, self.project)
        topic = recursive_replace_variables(test_context, stage_context, self.topic)
        topic_path = self.publisher.topic_path(project, topic)
        message = recursive_replace_variables(test_context, stage_context, self.message)
        attributes = recursive_replace_variables(test_context, stage_context, self.attributes) if self.attributes else {}

        self._log_debug(logger, topic=topic_path, attributes=attributes, message=message)
        future = self.publisher.publish(topic=topic_path, data=message.encode(), **attributes)

        stage_context['message_id'] = future.result()

    def _subscribe(self, logger: TestLogger, test_context: dict, stage_context: dict):
        self._authenticate()

        self.subscriber = SubscriberClient()

        project = recursive_replace_variables(test_context, stage_context, self.project)
        subscription = recursive_replace_variables(test_context, stage_context, self.subscription)
        subscription_path = self.subscriber.subscription_path(project, subscription)

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

    def _authenticate(self):
        credentials_path = os.getcwd() + '/credentials/gcp/gcp-credentials.json'
        if os.path.exists(credentials_path):
            self.credentials_path = credentials_path
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.credentials_path

    @staticmethod
    def _log_debug(logger: TestLogger, **parameters):
        logger.action_debug(json.dumps(parameters))

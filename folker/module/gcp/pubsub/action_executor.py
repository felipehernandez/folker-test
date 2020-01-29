import json
import os
import time

from google.cloud.pubsub_v1 import PublisherClient, SubscriberClient
from google.cloud.pubsub_v1.proto.pubsub_pb2 import PubsubMessage

from folker.logger import SequentialLogger
from folker.model.task import ActionExecutor
from folker.module.gcp.pubsub.data import PubSubMethod, PubSubStageData, PubSubActionData
from folker.util.variable import recursive_replace_variables


class PubSubActionExecutor(ActionExecutor):
    publisher: PublisherClient
    subscriber: SubscriberClient

    def __init__(self) -> None:
        super().__init__()
        self.logger = SequentialLogger()

        credentials_path = os.getcwd() + '/credentials/gcp/gcp-credentials.json'
        if os.path.exists(credentials_path):
            self.credentials_path = credentials_path
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.credentials_path

    def execute(self, stage_data: PubSubStageData, test_context: dict, stage_context: dict) -> (dict, dict):

        start = time.time()

        {
            PubSubMethod.PUBLISH: self._publish,
            PubSubMethod.SUBSCRIBE: self._subscribe
        }.get(stage_data.action.method)(stage_data.action, test_context, stage_context)

        end = time.time()
        stage_context['elapsed_time'] = int((end - start) * 1000)

        return test_context, stage_context

    def _publish(self, action: PubSubActionData, test_context: dict, stage_context: dict):
        self.publisher = PublisherClient()

        project = recursive_replace_variables(test_context, stage_context, action.project)
        topic = recursive_replace_variables(test_context, stage_context, action.topic)
        topic_path = self.publisher.topic_path(project, topic)
        message = recursive_replace_variables(test_context, stage_context, action.message)
        attributes = recursive_replace_variables(test_context, stage_context, action.attributes)

        self._log_debug(topic=topic_path, attributes=attributes, message=message)
        future = self.publisher.publish(topic=topic_path, data=message.encode(), **attributes)

        stage_context['message_id'] = future.result()

    def _subscribe(self, action: PubSubActionData, test_context: dict, stage_context: dict):
        self.subscriber = SubscriberClient()

        project = recursive_replace_variables(test_context, stage_context, action.project)
        subscription = recursive_replace_variables(test_context, stage_context, action.subscription)
        subscription_path = self.subscriber.subscription_path(project, subscription)

        self._log_debug(subscription=subscription_path, ack=action.ack)
        response = self.subscriber.pull(subscription=subscription_path, max_messages=1)

        for message in response.received_messages:
            message: PubsubMessage
            stage_context['ack_id'] = message.ack_id
            stage_context['message_id'] = message.message.message_id
            stage_context['publish_time'] = message.message.publish_time
            stage_context['attributes'] = message.message.attributes
            stage_context['message_content'] = message.message.data.decode('UTF-8')

            if action.ack:
                self.subscriber.acknowledge(subscription_path, [message.ack_id])

    def _log_debug(self, **parameters):
        self.logger.action_debug(json.dumps(parameters))

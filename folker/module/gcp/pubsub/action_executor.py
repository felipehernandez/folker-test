import os
import time

from google.cloud.pubsub_v1 import PublisherClient, SubscriberClient

from folker.model.task import ActionExecutor
from folker.module.gcp.pubsub.data import PubSubMethod, PubSubStageData, PubSubActionData


class PubSubActionExecutor(ActionExecutor):
    publisher: PublisherClient
    subscriber: SubscriberClient

    def __init__(self) -> None:
        super().__init__()

        credentials_path = os.getcwd() + '/credentials/gcp/gcp-credentials.json'
        if os.path.exists(credentials_path):
            self.credentials_path = credentials_path
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.credentials_path

        self.publisher = PublisherClient()
        self.subscriber = SubscriberClient()

    def execute(self, stage_data: PubSubStageData, test_context: dict, stage_context: dict) -> (dict, dict):
        start = time.time()

        {
            PubSubMethod.PUBLISH: self._publish,
            PubSubMethod.SUBSCRIBE: self._subscribe
        }.get(stage_data.action.method)(stage_data.action, stage_context)

        end = time.time()
        stage_context['elapsed_time'] = int((end - start) * 1000)

        return test_context, stage_context

    def _publish(self, action: PubSubActionData, stage_context: dict):
        topic_path = self.publisher.topic_path(action.project, action.topic)
        future = self.publisher.publish(topic=topic_path, data=action.message.encode())

        stage_context['message_id'] = future.result()

    def _subscribe(self, action: PubSubActionData, stage_context: dict):
        subscription_path = self.subscriber.subscription_path(action.project, action.subscription)
        response = self.subscriber.pull(subscription=subscription_path, max_messages=1)
        for message in response.received_messages:
            stage_context['message_id'] = message.ack_id
            stage_context['message_content'] = message.message.data.decode('UTF-8')

            if action.ack:
                self.subscriber.acknowledge(subscription_path, [message.ack_id])

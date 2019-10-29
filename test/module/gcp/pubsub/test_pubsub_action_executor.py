from unittest import TestCase
from unittest.mock import patch, Mock

from folker.module.gcp.pubsub.action_executor import PubSubActionExecutor
from folker.module.gcp.pubsub.data import PubSubStageData


class TestPubSubActionExecutor(TestCase):

    @patch('folker.module.gcp.pubsub.action_executor.SubscriberClient')
    @patch('folker.module.gcp.pubsub.action_executor.PublisherClient')
    def test_simple_publish_execution(self, MockPublisher, MockSubscriber):
        executor = PubSubActionExecutor()

        stage_data = PubSubStageData(id='1',
                                     name='pubsub_publish_stage',
                                     type='PUBSUB',
                                     action={
                                         'method': 'PUBLISH',
                                         'project': 'a-project',
                                         'topic': 'a-topic',
                                         'message': 'Hello world'
                                     })
        MockPublisher.return_value.topic_path.return_value = 'topic-path'
        future = Mock()
        MockPublisher.return_value.publish.return_value = future
        future.result.return_value = 'message-id'

        test_context, stage_context = executor.execute(stage_data, {}, {})

        self.assertEqual({}, test_context)
        self.assertTrue('elapsed_time' in stage_context)
        self.assertEqual('message-id', stage_context['message_id'])
        MockPublisher.return_value.publish.assert_called_with(topic='topic-path', data='Hello world'.encode())

    @patch('folker.module.gcp.pubsub.action_executor.SubscriberClient')
    @patch('folker.module.gcp.pubsub.action_executor.PublisherClient')
    def test_simple_ack_subscription_execution(self, MockPublisher, MockSubscriber):
        executor = PubSubActionExecutor()

        stage_data = PubSubStageData(id='1',
                                     name='pubsub_publish_stage',
                                     type='PUBSUB',
                                     action={
                                         'method': 'SUBSCRIBE',
                                         'project': 'a-project',
                                         'subscription': 'a-subscription',
                                         'ack': True
                                     })
        MockSubscriber.return_value.subscription_path.return_value = 'subscription-path'
        received_message = Mock()
        MockSubscriber.return_value.pull.return_value.received_messages = [received_message]
        received_message.ack_id = 'ack-id'
        received_message.message.data.decode.return_value = 'a-message'

        test_context, stage_context = executor.execute(stage_data, {}, {})

        self.assertEqual({}, test_context)
        self.assertTrue('elapsed_time' in stage_context)
        self.assertEqual('ack-id', stage_context['message_id'])
        self.assertEqual('a-message', stage_context['message_content'])
        MockSubscriber.return_value.acknowledge.assert_called_with('subscription-path', ['ack-id'])

    @patch('folker.module.gcp.pubsub.action_executor.SubscriberClient')
    @patch('folker.module.gcp.pubsub.action_executor.PublisherClient')
    def test_simple_nack_subscription_execution(self, MockPublisher, MockSubscriber):
        executor = PubSubActionExecutor()

        stage_data = PubSubStageData(id='1',
                                     name='pubsub_publish_stage',
                                     type='PUBSUB',
                                     action={
                                         'method': 'SUBSCRIBE',
                                         'project': 'a-project',
                                         'subscription': 'a-subscription',
                                         'ack': True
                                     })
        MockSubscriber.return_value.subscription_path.return_value = 'subscription-path'
        received_message = Mock()
        MockSubscriber.return_value.pull.return_value.received_messages = [received_message]
        received_message.ack_id = 'ack-id'
        received_message.message.data.decode.return_value = 'a-message'

        test_context, stage_context = executor.execute(stage_data, {}, {})

        self.assertEqual({}, test_context)
        self.assertTrue('elapsed_time' in stage_context)
        self.assertEqual('ack-id', stage_context['message_id'])
        self.assertEqual('a-message', stage_context['message_content'])
        self.assertFalse(MockSubscriber.return_value.acknowledge.assert_called())

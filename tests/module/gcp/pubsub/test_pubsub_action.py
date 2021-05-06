from unittest.mock import patch, Mock

import pytest
from pytest import raises

from folker.model.context import Context
from folker.model.error.load import InvalidSchemaDefinitionException
from folker.module.gcp.pubsub.action import PubSubStageAction, PubSubMethod


class TestPubSubAction:
    action: PubSubStageAction

    @pytest.fixture(autouse=True)
    def setup(self):
        self.action = PubSubStageAction()
        yield

    def test_validate_correct_publish(self):
        self.action.method = PubSubMethod.PUBLISH
        self.action.project = 'a-project'
        self.action.topic = 'a-topic'
        self.action.attributes = {'an-attribute': 'value'}
        self.action.message = 'message'

        self.action.validate()

    def test_validate_correct_publish_minimum(self):
        self.action.method = PubSubMethod.PUBLISH
        self.action.project = 'a-project'
        self.action.topic = 'a-topic'
        self.action.message = 'message'

        self.action.validate()

    def test_validate_correct_subscribe(self):
        self.action.method = PubSubMethod.SUBSCRIBE
        self.action.project = 'a-project'
        self.action.subscription = 'a-subscription'
        self.action.ack = True

        self.action.validate()

    def test_validate_correct_subscribe_minimum(self):
        self.action.method = PubSubMethod.SUBSCRIBE
        self.action.project = 'a-project'
        self.action.subscription = 'a-subscription'

        self.action.validate()

    def test_validate_missing_attribute_method(self):
        self.action.project = 'a-project'
        self.action.topic = 'a-topic'
        self.action.message = 'message'

        with raises(InvalidSchemaDefinitionException) as execution_context:
            self.action.validate()

        assert 'action.method' in execution_context.value.details['missing_fields']

    def test_validate_missing_attribute_project(self):
        self.action.method = PubSubMethod.PUBLISH
        self.action.topic = 'a-topic'
        self.action.message = 'message'

        with raises(InvalidSchemaDefinitionException) as execution_context:
            self.action.validate()

        assert ('action.project' in execution_context.value.details['missing_fields'])

    def test_validate_missing_attribute_topic(self):
        self.action.method = PubSubMethod.PUBLISH
        self.action.project = 'a-project'
        self.action.message = 'message'

        with raises(InvalidSchemaDefinitionException) as execution_context:
            self.action.validate()

        assert ('action.topic' in execution_context.value.details['missing_fields'])

    def test_validate_missing_attribute_message(self):
        self.action.method = PubSubMethod.PUBLISH
        self.action.project = 'a-project'
        self.action.topic = 'a-topic'

        with raises(InvalidSchemaDefinitionException) as execution_context:
            self.action.validate()

        assert ('action.message' in execution_context.value.details['missing_fields'])

    def test_validate_missing_attribute_subscription(self):
        self.action.method = PubSubMethod.SUBSCRIBE
        self.action.project = 'a-project'

        with raises(InvalidSchemaDefinitionException) as execution_context:
            self.action.validate()

        assert ('action.subscription'
                in execution_context.value.details['missing_fields'])

    @patch('os.path.exists')
    @patch('folker.module.gcp.pubsub.action.SubscriberClient')
    @patch('folker.module.gcp.pubsub.action.PublisherClient')
    def test_simple_publish_execution(self, MockPublisher, MockSubscriber, mock_os):
        logger = Mock()
        mock_os.return_value = True

        self.action.method = PubSubMethod.PUBLISH
        self.action.project = 'a-project'
        self.action.topic = 'a-topic'
        self.action.message = 'Hello world'

        MockPublisher.return_value.topic_path.return_value = 'topic-path'
        future = Mock()
        MockPublisher.return_value.publish.return_value = future
        future.result.return_value = 'message-id'

        context = self.action.execute(logger, context=Context())

        assert {} == context.test_variables
        assert 'elapsed_time' in context.stage_variables
        assert 'message-id', context.stage_variables['message_id']
        MockPublisher.return_value.publish.assert_called_with(topic='topic-path',
                                                              data='Hello world')

    @patch('os.path.exists')
    @patch('folker.module.gcp.pubsub.action.SubscriberClient')
    @patch('folker.module.gcp.pubsub.action.PublisherClient')
    def test_simple_ack_subscription_execution(self, MockPublisher, MockSubscriber, mock_os):
        logger = Mock()
        mock_os.return_value = True

        self.action.method = PubSubMethod.SUBSCRIBE
        self.action.project = 'a-project'
        self.action.subscription = 'a-subscription'
        self.action.ack = True

        MockSubscriber.return_value.subscription_path.return_value = 'subscription-path'
        received_message = Mock()
        MockSubscriber.return_value.pull.return_value.received_messages = [received_message]
        received_message.ack_id = 'ack-id'
        received_message.message.message_id = 'message-id'
        received_message.message.data.decode.return_value = 'a-message'

        context = self.action.execute(logger, context=Context())

        assert {} == context.test_variables
        assert 'elapsed_time' in context.stage_variables
        assert 'ack-id' == context.stage_variables['ack_id']
        assert 'message-id' == context.stage_variables['message_id']
        assert 'a-message' == context.stage_variables['message_content']
        MockSubscriber.return_value.acknowledge.assert_called_with(
            request={"subscription": 'subscription-path', "ack_ids": ['ack-id']})

    @patch('os.path.exists')
    @patch('folker.module.gcp.pubsub.action.SubscriberClient')
    @patch('folker.module.gcp.pubsub.action.PublisherClient')
    def test_simple_nack_subscription_execution(self, MockPublisher, MockSubscriber, mock_os):
        logger = Mock()
        mock_os.return_value = True

        self.action.method = PubSubMethod.SUBSCRIBE
        self.action.project = 'a-project'
        self.action.subscription = 'a-subscription'
        self.action.ack = False

        MockSubscriber.return_value.subscription_path.return_value = 'subscription-path'
        received_message = Mock()
        MockSubscriber.return_value.pull.return_value.received_messages = [received_message]
        received_message.ack_id = 'ack-id'
        received_message.message.message_id = 'message-id'
        received_message.message.data.decode.return_value = 'a-message'

        context = self.action.execute(logger, context=Context())

        assert {} == context.test_variables
        assert 'elapsed_time' in context.stage_variables
        assert 'ack-id' == context.stage_variables['ack_id']
        assert 'message-id' == context.stage_variables['message_id']
        assert 'a-message' == context.stage_variables['message_content']
        assert not MockSubscriber.return_value.acknowledge.assert_not_called()

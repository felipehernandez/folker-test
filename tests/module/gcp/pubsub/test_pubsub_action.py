from unittest.mock import patch, Mock

import pytest

from folker.model.context import Context
from folker.module.gcp.pubsub.action import (
    PubSubStageAction,
    PubSubMethod,
    PubSubStagePublishAction,
    PubSubStageSubscribeAction,
)


@pytest.mark.action_gcp_pubsub
class TestPubSubStagePublishAction:
    @patch("os.path.exists")
    @patch("folker.module.gcp.pubsub.action.PublisherClient")
    def test_simple_publish_execution(
        self, MockPublisher, mock_os, plain_console_test_logger_on_trace
    ):
        mock_os.return_value = True
        action = PubSubStagePublishAction(
            method=PubSubMethod.PUBLISH.name,
            project="a-project",
            topic="a-topic",
            message="Hello world",
        )

        MockPublisher.return_value.topic_path.return_value = "topic-path"
        future = Mock()
        MockPublisher.return_value.publish.return_value = future
        future.result.return_value = "message-id"

        context = action.execute(
            logger=plain_console_test_logger_on_trace, context=Context()
        )

        assert {} == context.test_variables
        assert "elapsed_time" in context.stage_variables
        assert "message-id", context.stage_variables["message_id"]
        MockPublisher.return_value.publish.assert_called_with(
            topic="topic-path", data="Hello world".encode()
        )


@pytest.mark.action_gcp_pubsub
class TestPubSubStageSubscribeAction:
    @patch("os.path.exists")
    @patch("folker.module.gcp.pubsub.action.SubscriberClient")
    def test_simple_ack_subscription_execution(
        self, MockSubscriber, mock_os, plain_console_test_logger_on_trace
    ):
        mock_os.return_value = True

        action = PubSubStageSubscribeAction(
            method=PubSubMethod.SUBSCRIBE.name,
            project="a-project",
            subscription="a-subscription",
            ack=True,
        )

        MockSubscriber.return_value.subscription_path.return_value = "subscription-path"
        received_message = Mock()
        MockSubscriber.return_value.pull.return_value.received_messages = [
            received_message
        ]
        received_message.ack_id = "ack-id"
        received_message.message.message_id = "message-id"
        received_message.message.data.decode.return_value = "a-message"

        context = action.execute(
            logger=plain_console_test_logger_on_trace, context=Context()
        )

        assert {} == context.test_variables
        assert "elapsed_time" in context.stage_variables
        assert "ack-id" == context.stage_variables["ack_id"]
        assert "message-id" == context.stage_variables["message_id"]
        assert "a-message" == context.stage_variables["message_content"]
        MockSubscriber.return_value.acknowledge.assert_called_with(
            subscription="subscription-path", ack_ids=["ack-id"]
        )

    @patch("os.path.exists")
    @patch("folker.module.gcp.pubsub.action.SubscriberClient")
    def test_simple_nack_subscription_execution(
        self, MockSubscriber, mock_os, plain_console_test_logger_on_trace
    ):
        mock_os.return_value = True

        action = PubSubStageSubscribeAction(
            method=PubSubMethod.SUBSCRIBE.name,
            project="a-project",
            subscription="a-subscription",
            ack=False,
        )

        MockSubscriber.return_value.subscription_path.return_value = "subscription-path"
        received_message = Mock()
        MockSubscriber.return_value.pull.return_value.received_messages = [
            received_message
        ]
        received_message.ack_id = "ack-id"
        received_message.message.message_id = "message-id"
        received_message.message.data.decode.return_value = "a-message"

        context = action.execute(
            logger=plain_console_test_logger_on_trace, context=Context()
        )

        assert {} == context.test_variables
        assert "elapsed_time" in context.stage_variables
        assert "ack-id" == context.stage_variables["ack_id"]
        assert "message-id" == context.stage_variables["message_id"]
        assert "a-message" == context.stage_variables["message_content"]
        assert not MockSubscriber.return_value.acknowledge.assert_not_called()

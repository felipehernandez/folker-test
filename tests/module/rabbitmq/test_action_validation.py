import pytest

from folker.module.rabbitmq.action import (RabbitMQMethod, RabbitMQStageAction,
                                           RabbitMQStagePublishAction,
                                           RabbitMQStageSubscribeAction)


@pytest.mark.action_correctness
@pytest.mark.action_rabbitmq
class TestRabbitMQActionValidation:
    def test_validate_missing_attribute_method(self):
        action = RabbitMQStageAction(
            host="a-host", exchange="an-exchange", message="A message"
        )

        assert not action
        assert not action.validation_report
        assert "action.method" in action.validation_report.missing_fields


@pytest.mark.action_correctness
@pytest.mark.action_rabbitmq
class TestRabbitMQPublishActionValidation:
    def test_validate_publish_with_message_correct(self):
        action = RabbitMQStagePublishAction(
            method=RabbitMQMethod.PUBLISH.name,
            host="a-host",
            exchange="an-exchange",
            message="A message",
        )

        assert action
        assert action.validation_report

    def test_validate_correct_publish_minimum_message(self):
        action = RabbitMQStagePublishAction(
            method=RabbitMQMethod.PUBLISH.name,
            host="a-host",
            exchange="an-exchange",
            message="a-message",
        )

        assert action
        assert action.validation_report

    def test_validate_missing_attribute_method(self):
        action = RabbitMQStageAction(
            host="a-host", exchange="an-exchange", message="A message"
        )

        assert not action
        assert not action.validation_report
        assert "action.method" in action.validation_report.missing_fields

    def test_validate_missing_attribute_host(self):
        action = RabbitMQStagePublishAction(
            method=RabbitMQMethod.PUBLISH.name,
            exchange="an-exchange",
            message="A message",
        )

        assert not action
        assert not action.validation_report
        assert "action.host" in action.validation_report.missing_fields

    def test_validate_missing_attribute_exchange(self):
        action = RabbitMQStagePublishAction(
            method=RabbitMQMethod.PUBLISH.name, host="a-host", message="A message"
        )

        assert not action
        assert not action.validation_report
        assert "action.exchange" in action.validation_report.missing_fields

    def test_validate_missing_attribute_message(self):
        action = RabbitMQStagePublishAction(
            method=RabbitMQMethod.PUBLISH.name, host="a-host", exchange="an-exchange"
        )

        assert not action
        assert not action.validation_report
        assert "action.message" in action.validation_report.missing_fields


@pytest.mark.action_correctness
@pytest.mark.action_rabbitmq
class TestRabbitMQSubscribeActionValidation:
    def test_validate_correct_subscribe(self):
        action = RabbitMQStageSubscribeAction(
            method=RabbitMQMethod.SUBSCRIBE.name,
            host="a-host",
            queue="a_queue",
            ack=True,
        )

        assert action
        assert action.validation_report

    def test_validate_correct_subscribe_minimum(self):
        action = RabbitMQStageSubscribeAction(
            method=RabbitMQMethod.SUBSCRIBE.name, host="a-host", queue="a_queue"
        )

        assert action
        assert action.validation_report

    def test_validate_missing_attribute_queue(self):
        action = RabbitMQStageSubscribeAction(
            method=RabbitMQMethod.SUBSCRIBE.name, host="a-host"
        )

        assert not action
        assert not action.validation_report
        assert "action.queue" in action.validation_report.missing_fields

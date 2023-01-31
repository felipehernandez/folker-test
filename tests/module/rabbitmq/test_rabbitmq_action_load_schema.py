import pytest
from yaml import SafeLoader, load

from folker.module.rabbitmq.action import (RabbitMQMethod, RabbitMQStageAction,
                                           RabbitMQStagePublishAction)
from folker.module.rabbitmq.schema import RabbitMQActionSchema


@pytest.mark.action_rabbitmq
class TestRabbitMQStageLoadSchema:
    schema = RabbitMQActionSchema()

    def test_given_basic_publish(self):
        original_yaml = """
            type: RABBITMQ
            method: PUBLISH
            host: http://a_host
            port: '5672'
            vhost: test
            exchange: an-exchange
            message: a message
        """

        definition = load(original_yaml, Loader=SafeLoader)
        loaded_action: RabbitMQStageAction = self.schema.load(definition)

        assert type(loaded_action) is RabbitMQStagePublishAction

        assert loaded_action.method is RabbitMQMethod.PUBLISH
        assert loaded_action.host == 'http://a_host'
        assert loaded_action.port == '5672'
        assert loaded_action.vhost == 'test'
        assert loaded_action.exchange == 'an-exchange'
        assert loaded_action.message == 'a message'

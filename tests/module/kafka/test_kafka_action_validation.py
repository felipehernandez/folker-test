import pytest
from pytest import raises

from folker.model.error.load import InvalidSchemaDefinitionException
from folker.module.kafka.action import KafkaStageAction, KafkaMethod


class TestKafkaActionValidation:
    action: KafkaStageAction

    @pytest.fixture(autouse=True)
    def setup(self):
        self.action = KafkaStageAction()
        yield

    def test_validate_correct_publish_with_key(self):
        self.action.method = KafkaMethod.PUBLISH
        self.action.host = 'a-host'
        self.action.topic = 'a-topic'
        self.action.headers = {'an-attribute': 'value'}
        self.action.key = 'a-key'

        self.action.validate()

    def test_validate_correct_publish_with_message(self):
        self.action.method = KafkaMethod.PUBLISH
        self.action.host = 'a-host'
        self.action.topic = 'a-topic'
        self.action.headers = {'an-attribute': 'value'}
        self.action.message = 'a-message'

        self.action.validate()

    def test_validate_correct_publish_with_message_and_key(self):
        self.action.method = KafkaMethod.PUBLISH
        self.action.host = 'a-host'
        self.action.topic = 'a-topic'
        self.action.headers = {'an-attribute': 'value'}
        self.action.key = 'a-key'
        self.action.message = 'a-message'

        self.action.validate()

    def test_validate_correct_publish_minimum_key(self):
        self.action.method = KafkaMethod.PUBLISH
        self.action.host = 'a-host'
        self.action.topic = 'a-topic'
        self.action.key = 'a-key'

        self.action.validate()

    def test_validate_correct_publish_minimum_message(self):
        self.action.method = KafkaMethod.PUBLISH
        self.action.host = 'a-host'
        self.action.topic = 'a-topic'
        self.action.message = 'a-message'

        self.action.validate()

    def test_validate_correct_publish_minimum_message_and_key(self):
        self.action.method = KafkaMethod.PUBLISH
        self.action.host = 'a-host'
        self.action.topic = 'a-topic'
        self.action.key = 'a-key'
        self.action.message = 'a-message'

        self.action.validate()

    def test_validate_correct_subscribe(self):
        self.action.method = KafkaMethod.SUBSCRIBE
        self.action.host = 'a-host'
        self.action.topic = 'a-topic'
        self.action.group = 'a-group'

        self.action.validate()

    def test_validate_correct_subscribe_minimum(self):
        self.action.method = KafkaMethod.SUBSCRIBE
        self.action.host = 'a-host'
        self.action.topic = 'a-topic'

        self.action.validate()

    def test_validate_missing_attribute_method(self):
        self.action.host = 'a-host'
        self.action.topic = 'a-topic'

        with raises(InvalidSchemaDefinitionException) as execution_context:
            self.action.validate()

        assert 'action.method' in execution_context.value.details['missing_fields']

    def test_validate_missing_attribute_host(self):
        self.action.method = KafkaMethod.PUBLISH
        self.action.topic = 'a-topic'

        with raises(InvalidSchemaDefinitionException) as execution_context:
            self.action.validate()

        assert ('action.host' in execution_context.value.details['missing_fields'])

    def test_validate_missing_attribute_topic(self):
        self.action.method = KafkaMethod.PUBLISH
        self.action.host = 'a-host'

        with raises(InvalidSchemaDefinitionException) as execution_context:
            self.action.validate()

        assert ('action.topic' in execution_context.value.details['missing_fields'])

    def test_validate_missing_attribute_publish_key_and_message(self):
        self.action.method = KafkaMethod.PUBLISH
        self.action.host = 'a-host'
        self.action.topic = 'a-topic'

        with raises(InvalidSchemaDefinitionException) as execution_context:
            self.action.validate()

        assert ('action.key' in execution_context.value.details['missing_fields'])
        assert ('action.message' in execution_context.value.details['missing_fields'])

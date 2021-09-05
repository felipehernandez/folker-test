from unittest.mock import patch, Mock

import pytest

from folker.model.context import Context
from folker.module.kafka.action import KafkaStageAction, KafkaMethod


@pytest.mark.action_kafka
class TestKafkaAction:
    action: KafkaStageAction

    @pytest.fixture(autouse=True)
    def setup(self):
        self.action = KafkaStageAction()
        yield

    @patch('folker.module.kafka.action.KafkaProducer')
    def test_simple_publish_execution(self, KafkaProducer, plain_console_test_logger_on_trace):
        logger = plain_console_test_logger_on_trace

        self.action.method = KafkaMethod.PUBLISH
        self.action.host = 'a-host'
        self.action.topic = 'a-topic'
        self.action.key = 'a-key'

        mock_future = Mock()
        KafkaProducer.return_value.send.return_value = mock_future

        mock_record_metadata = Mock()
        mock_future.get.return_value = mock_record_metadata
        mock_record_metadata.topic = 'a-topic'
        mock_record_metadata.partition = 'a-partition'
        mock_record_metadata.timestamp = 'a-timestamp'
        mock_record_metadata.offset = 'an-offset'

        context = self.action.execute(logger=logger, context=Context())

        KafkaProducer.assert_called_once_with(bootstrap_servers=['a-host'])
        KafkaProducer.return_value.send.assert_called_with(topic='a-topic',
                                                           key='a-key'.encode(),
                                                           value=None,
                                                           headers=[])
        assert context.test_variables == {}
        assert 'elapsed_time' in context.stage_variables
        assert context.stage_variables['topic'] == 'a-topic'
        assert context.stage_variables['partition'] == 'a-partition'
        assert context.stage_variables['timestamp'] == 'a-timestamp'
        assert context.stage_variables['offset'] == 'an-offset'

    @patch('folker.module.kafka.action.KafkaConsumer')
    def test_simple_subscription_execution(self, KafkaConsumer, plain_console_test_logger_on_trace):
        self.action.method = KafkaMethod.SUBSCRIBE
        self.action.project = 'a-project'
        self.action.host = 'a-host'
        self.action.topic = 'a-topic'

        message1 = Mock()
        message1.headers = {}
        message1.key = 'a-key'.encode()
        message1.offset = 1
        message1.timestamp = 'a-timestamp'
        message1.topic = 'a-topic'
        message1.value = 'a-message'.encode()
        KafkaConsumer.return_value = [message1]

        context = self.action.execute(logger=(plain_console_test_logger_on_trace),
                                      context=Context())

        KafkaConsumer.assert_called_once_with('a-topic',
                                              group_id=None,
                                              auto_offset_reset='earliest',
                                              consumer_timeout_ms=10000,
                                              bootstrap_servers=['a-host'])

        assert context.test_variables == {}
        assert 'elapsed_time' in context.stage_variables
        assert 'messages' in context.stage_variables

        assert context.stage_variables['messages'][0]['headers'] == {}
        assert context.stage_variables['messages'][0]['key'] == 'a-key'
        assert context.stage_variables['messages'][0]['offset'] == 1
        assert context.stage_variables['messages'][0]['timestamp'] == 'a-timestamp'
        assert context.stage_variables['messages'][0]['topic'] == 'a-topic'
        assert context.stage_variables['messages'][0]['message'] == 'a-message'

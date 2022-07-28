from unittest.mock import patch, Mock

import pytest

from folker.model.context import Context
from folker.module.rabbitmq.action import RabbitMQStageAction, RabbitMQMethod


@pytest.mark.action_rabbitmq
class TestRabbitMQAction:
    action: RabbitMQStageAction

    @pytest.fixture(autouse=True)
    def setup(self):
        self.action = RabbitMQStageAction()
        yield

    @patch('folker.module.rabbitmq.action.pika.ConnectionParameters')
    @patch('folker.module.rabbitmq.action.pika.BlockingConnection')
    def test_simple_publish_execution(self,
                                      BlockingConnection,
                                      ConnectionParameters,
                                      plain_console_test_logger_on_trace):
        logger = plain_console_test_logger_on_trace

        self.action.method = RabbitMQMethod.PUBLISH
        self.action.host = 'a-host'
        self.action.exchange = 'an-exchange'
        self.action.vhost = 'a-virtual-host'
        self.action.message = 'a-message'

        mocked_conn_params = Mock()
        ConnectionParameters.return_value = mocked_conn_params

        context = self.action.execute(logger=logger, context=Context())

        ConnectionParameters.assert_called_once_with(host='a-host', virtual_host='a-virtual-host')
        BlockingConnection.assert_called_once_with(mocked_conn_params)

        BlockingConnection.return_value.channel.return_value.basic_publish.assert_called_with(
            exchange='an-exchange',
            routing_key='',
            body='a-message'.encode())

        assert context.test_variables == {}
        assert 'elapsed_time' in context.stage_variables
        assert context.stage_variables['published'] == True

    @patch('folker.module.rabbitmq.action.pika.ConnectionParameters')
    @patch('folker.module.rabbitmq.action.pika.BlockingConnection')
    def test_simple_subscription_execution(self,
                                           BlockingConnection,
                                           ConnectionParameters,
                                           plain_console_test_logger_on_trace):
        logger = plain_console_test_logger_on_trace

        self.action.method = RabbitMQMethod.SUBSCRIBE
        self.action.host = 'a-host'
        self.action.queue = 'a-queue'
        self.action.ack = True

        mocked_conn_params = Mock()
        ConnectionParameters.return_value = mocked_conn_params
        mock_future = Mock()
        BlockingConnection.return_value \
            .channel.return_value = mock_future

        BlockingConnection.return_value \
            .channel.return_value \
            .basic_get.return_value = None, None, 'a-message'.encode()

        context = self.action.execute(logger=logger, context=Context())

        BlockingConnection.return_value \
            .channel.return_value \
            .basic_get.assert_called_with(queue='a-queue', auto_ack=True)

        assert context.test_variables == {}
        assert 'elapsed_time' in context.stage_variables
        assert 'message' in context.stage_variables

        assert context.stage_variables['queue'] == 'a-queue'
        assert context.stage_variables['message'] == 'a-message'
        assert context.stage_variables['ack-ed'] == True

    @patch('folker.module.rabbitmq.action.pika.ConnectionParameters')
    @patch('folker.module.rabbitmq.action.pika.BlockingConnection')
    def test_simple_count(self,
                          BlockingConnection,
                          ConnectionParameters,
                          plain_console_test_logger_on_trace):
        logger = plain_console_test_logger_on_trace

        self.action.method = RabbitMQMethod.COUNT
        self.action.host = 'a-host'
        self.action.queue = 'a-queue'
        self.action.user = 'a_user'
        self.action.password = 'p4$$w0rD'

        mocked_conn_params = Mock()
        ConnectionParameters.return_value = mocked_conn_params
        mock_future = Mock()
        BlockingConnection.return_value \
            .channel.return_value = mock_future

        queue_declaration = Mock()
        BlockingConnection.return_value \
            .channel.return_value \
            .queue_declare.return_value = queue_declaration
        queue_declaration.method.message_count = 42

        context = self.action.execute(logger=logger, context=Context())

        BlockingConnection.return_value \
            .channel.return_value \
            .queue_declare.assert_called_with(queue='a-queue', passive=True)

        assert context.test_variables == {}
        assert 'elapsed_time' in context.stage_variables
        assert 'result' in context.stage_variables

        assert context.stage_variables['result'] == 42

    @patch('folker.module.rabbitmq.action.pika.ConnectionParameters')
    @patch('folker.module.rabbitmq.action.pika.BlockingConnection')
    def test_simple_clear(self,
                          BlockingConnection,
                          ConnectionParameters,
                          plain_console_test_logger_on_trace):
        logger = plain_console_test_logger_on_trace

        self.action.method = RabbitMQMethod.CLEAR
        self.action.host = 'a-host'
        self.action.queue = 'a-queue'
        self.action.user = 'a_user'
        self.action.password = 'p4$$w0rD'

        mocked_conn_params = Mock()
        ConnectionParameters.return_value = mocked_conn_params
        mock_future = Mock()
        BlockingConnection.return_value \
            .channel.return_value = mock_future

        queue_purge_result = Mock()
        BlockingConnection.return_value \
            .channel.return_value \
            .queue_purge.return_value = queue_purge_result
        queue_purge_result.method.message_count = 42

        context = self.action.execute(logger=logger, context=Context())

        BlockingConnection.return_value \
            .channel.return_value \
            .queue_purge.assert_called_with(queue='a-queue')

        assert context.test_variables == {}
        assert 'elapsed_time' in context.stage_variables
        assert 'result' in context.stage_variables

        assert context.stage_variables['result'] == True
        assert context.stage_variables['num_messages'] == 42

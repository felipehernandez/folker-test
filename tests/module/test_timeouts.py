from unittest.mock import Mock, patch

import psycopg2
import pytest
import requests

from folker.model import Context
from folker.module.graphql.action import GraphQLStageAction
from folker.module.gcp.pubsub.action import (PubSubStagePublishAction,
                                             PubSubStageSubscribeAction,
                                             PubSubStageSubscriptionsAction,
                                             PubSubStageTopicsAction)
from folker.module.gcp.pubsub.schema import PubSubActionSchema
from folker.module.graphql.schema import GraphQLActionSchema
from folker.module.grpc.action import GrpcStageAction
from folker.module.grpc.schema import GrpcActionSchema
from folker.module.postgres.action import PostgresStageSelectAction
from folker.module.postgres.schema import PostgresActionSchema
from folker.module.rabbitmq.action import RabbitMQStageCountAction, RabbitMQStagePublishAction
from folker.module.rabbitmq.schema import RabbitMQActionSchema
from folker.module.rest.action import RestStageAction, RestMethod
from folker.module.rest.schema import RestActionSchema
from folker.module.timeout import DEFAULT_TIMEOUT
from folker.module.zookeeper.action import ZookeeperStageExistsAction, ZookeeperStageGetAction
from folker.module.zookeeper.schema import ZookeeperActionSchema

# (action class, schema, minimal valid definition)
ACTIONS = [
    pytest.param(RestStageAction, RestActionSchema,
                 {'method': 'GET', 'host': 'h'}, id='rest'),
    pytest.param(PostgresStageSelectAction, PostgresActionSchema,
                 {'method': 'SELECT', 'host': 'h', 'port': '5432', 'user': 'u',
                  'password': 'p', 'database': 'd', 'sql': 's'}, id='postgres'),
    pytest.param(RabbitMQStageCountAction, RabbitMQActionSchema,
                 {'method': 'COUNT', 'host': 'h', 'queue': 'q'}, id='rabbitmq'),
    pytest.param(ZookeeperStageGetAction, ZookeeperActionSchema,
                 {'method': 'GET', 'host': 'h', 'node': '/n'}, id='zookeeper'),
    pytest.param(GraphQLStageAction, GraphQLActionSchema,
                 {'host': 'h', 'query': 'q'}, id='graphql'),
    pytest.param(GrpcStageAction, GrpcActionSchema,
                 {'host': 'h', 'package': 'p', 'stub': 's', 'method': 'm'}, id='grpc'),
    pytest.param(PubSubStagePublishAction, PubSubActionSchema,
                 {'method': 'PUBLISH', 'project': 'p', 'topic': 't', 'message': 'm'},
                 id='pubsub'),
]


@pytest.mark.parametrize('action_class, schema, definition', ACTIONS)
class TestActionTimeoutDefinition:
    def test_loaded_from_the_definition(self, action_class, schema, definition):
        action = schema().load({**definition, 'timeout': 5})

        assert action.timeout == 5

    def test_not_set_by_default(self, action_class, schema, definition):
        assert schema().load(definition).timeout is None

    def test_enrichment_overrides_only_when_defined(self, action_class, schema, definition):
        original = action_class(**definition, timeout=5)

        assert (original + action_class(timeout=9)).timeout == 9
        assert (original + action_class()).timeout == 5

    @pytest.mark.parametrize('timeout', [0, -1, 'soon', True])
    def test_invalid_timeout_is_a_wrong_field(self, action_class, schema, definition, timeout):
        action = action_class(**definition, timeout=timeout)

        assert not action
        assert 'action.timeout' in action.validation_report.wrong_fields

    def test_valid_timeout_passes_validation(self, action_class, schema, definition):
        assert action_class(**definition, timeout=2.5)


@pytest.mark.action_rest
class TestRestTimeout:
    @patch.object(requests, 'get')
    def test_default(self, requests_get, plain_console_test_logger_on_trace):
        action = RestStageAction(method='GET', host='h')
        action.method = RestMethod.GET

        action.execute(logger=plain_console_test_logger_on_trace, context=Context())

        assert requests_get.call_args.kwargs['timeout'] == DEFAULT_TIMEOUT

    @patch.object(requests, 'post')
    def test_custom(self, requests_post, plain_console_test_logger_on_trace):
        action = RestStageAction(method='POST', host='h', timeout=3)

        action.execute(logger=plain_console_test_logger_on_trace, context=Context())

        assert requests_post.call_args.kwargs['timeout'] == 3

    @patch.object(requests, 'get', side_effect=requests.exceptions.ConnectTimeout('too slow'))
    def test_timeout_is_reported_as_the_action_error(self, _, plain_console_test_logger_on_trace):
        action = RestStageAction(method='GET', host='h')

        context = action.execute(logger=plain_console_test_logger_on_trace, context=Context())

        assert isinstance(context.stage_variables['error'], requests.exceptions.ConnectTimeout)


@pytest.mark.action_postgres
class TestPostgresTimeout:
    def action(self, **fields):
        return PostgresStageSelectAction(method='SELECT', host='h', port='5432', user='u',
                                         password='p', database='d', sql='select 1', **fields)

    @patch('folker.module.postgres.action.psycopg2.connect')
    def test_default(self, connect, plain_console_test_logger_on_trace):
        connect.return_value.cursor.return_value.fetchall.return_value = []

        self.action().execute(logger=plain_console_test_logger_on_trace, context=Context())

        kwargs = connect.call_args.kwargs
        assert kwargs['connect_timeout'] == DEFAULT_TIMEOUT
        assert kwargs['options'] == f'-c statement_timeout={int(DEFAULT_TIMEOUT * 1000)}'

    @patch('folker.module.postgres.action.psycopg2.connect')
    def test_custom_is_rounded_up_for_connect(self, connect, plain_console_test_logger_on_trace):
        connect.return_value.cursor.return_value.fetchall.return_value = []

        self.action(timeout=2.5).execute(logger=plain_console_test_logger_on_trace,
                                         context=Context())

        kwargs = connect.call_args.kwargs
        assert kwargs['connect_timeout'] == 3
        assert kwargs['options'] == '-c statement_timeout=2500'

    @patch('folker.module.postgres.action.psycopg2.connect',
           side_effect=psycopg2.OperationalError('timeout expired'))
    def test_connection_failure_is_reported_as_the_action_error(
            self, _, plain_console_test_logger_on_trace):
        context = self.action().execute(logger=plain_console_test_logger_on_trace,
                                        context=Context())

        assert isinstance(context.stage_variables['error'], psycopg2.OperationalError)


@pytest.mark.action_rabbitmq
class TestRabbitMQTimeout:
    @pytest.mark.parametrize('fields, expected', [({}, DEFAULT_TIMEOUT), ({'timeout': 4}, 4)])
    @patch('folker.module.rabbitmq.action.pika.BlockingConnection')
    @patch('folker.module.rabbitmq.action.pika.ConnectionParameters')
    def test_connection_timeouts(self, parameters, _, fields, expected,
                                 plain_console_test_logger_on_trace):
        action = RabbitMQStagePublishAction(method='PUBLISH', host='h', exchange='e',
                                            message='m', **fields)

        action.execute(logger=plain_console_test_logger_on_trace, context=Context())

        kwargs = parameters.call_args.kwargs
        assert kwargs['socket_timeout'] == expected
        assert kwargs['stack_timeout'] == expected
        assert kwargs['blocked_connection_timeout'] == expected


@pytest.mark.action_zookeeper
class TestZookeeperTimeout:
    @pytest.mark.parametrize('fields, expected', [({}, DEFAULT_TIMEOUT), ({'timeout': 4}, 4)])
    @patch('folker.module.zookeeper.action.KazooClient')
    def test_start_timeout(self, kazoo, fields, expected, plain_console_test_logger_on_trace):
        action = ZookeeperStageExistsAction(method='EXISTS', host='h', node='/n', **fields)

        action.execute(logger=plain_console_test_logger_on_trace, context=Context())

        kazoo.return_value.start.assert_called_once_with(timeout=expected)

    @patch('folker.module.zookeeper.action.KazooClient')
    def test_client_is_stopped_when_the_connection_times_out(
            self, kazoo, plain_console_test_logger_on_trace):
        kazoo.return_value.start.side_effect = TimeoutError('Connection time-out')
        action = ZookeeperStageExistsAction(method='EXISTS', host='h', node='/n')

        with pytest.raises(TimeoutError):
            action.execute(logger=plain_console_test_logger_on_trace, context=Context())

        kazoo.return_value.stop.assert_called_once()


@pytest.mark.action_graphql
class TestGraphQLTimeout:
    @pytest.mark.parametrize('fields, expected', [({}, DEFAULT_TIMEOUT), ({'timeout': 4}, 4)])
    @patch('folker.module.graphql.action.Client')
    @patch('folker.module.graphql.action.gql')
    @patch('folker.module.graphql.action.RequestsHTTPTransport')
    def test_transport_timeout(self, transport, _gql, _client, fields, expected,
                               plain_console_test_logger_on_trace):
        action = GraphQLStageAction(host='h', query='q', **fields)

        action.execute(logger=plain_console_test_logger_on_trace, context=Context())

        assert transport.call_args.kwargs['timeout'] == expected


@pytest.mark.action_grpc
class TestGrpcTimeout:
    @pytest.mark.parametrize('fields, expected', [({}, DEFAULT_TIMEOUT), ({'timeout': 4}, 4)])
    @patch('folker.module.grpc.action.grpc.insecure_channel')
    @patch('builtins.__import__')
    def test_call_deadline(self, importer, _channel, fields, expected,
                           plain_console_test_logger_on_trace):
        remote_method = importer.return_value.Stub.return_value.Call
        remote_method.return_value = 'response'
        action = GrpcStageAction(host='h', package='p', stub='Stub', method='Call',
                                 data='d', **fields)

        action.execute(logger=plain_console_test_logger_on_trace, context=Context())

        remote_method.assert_called_once_with('d', timeout=expected)


@pytest.mark.action_gcp_pubsub
class TestPubSubTimeout:
    @pytest.fixture(autouse=True)
    def no_credentials(self):
        with patch('folker.module.gcp.pubsub.action.PubSubStageAction._authenticate'):
            yield

    @pytest.mark.parametrize('fields, expected', [({}, DEFAULT_TIMEOUT), ({'timeout': 4}, 4)])
    @patch('folker.module.gcp.pubsub.action.PublisherClient')
    def test_publish(self, publisher, fields, expected, plain_console_test_logger_on_trace):
        publisher.return_value.topic_path.return_value = 'topic-path'
        future = publisher.return_value.publish.return_value
        action = PubSubStagePublishAction(method='PUBLISH', project='p', topic='t',
                                          message='m', **fields)

        action.execute(logger=plain_console_test_logger_on_trace, context=Context())

        future.result.assert_called_once_with(timeout=expected)

    @pytest.mark.parametrize('fields, expected', [({}, DEFAULT_TIMEOUT), ({'timeout': 4}, 4)])
    @patch('folker.module.gcp.pubsub.action.SubscriberClient')
    def test_subscribe_pull_and_ack(self, subscriber, fields, expected,
                                    plain_console_test_logger_on_trace):
        client = subscriber.return_value
        client.subscription_path.return_value = 'subscription-path'
        client.pull.return_value.received_messages = [Mock()]
        action = PubSubStageSubscribeAction(method='SUBSCRIBE', project='p',
                                            subscription='s', ack=True, **fields)

        action.execute(logger=plain_console_test_logger_on_trace, context=Context())

        assert client.pull.call_args.kwargs['timeout'] == expected
        assert client.acknowledge.call_args.kwargs['timeout'] == expected

    @pytest.mark.parametrize('fields, expected', [({}, DEFAULT_TIMEOUT), ({'timeout': 4}, 4)])
    @patch('folker.module.gcp.pubsub.action.PublisherClient')
    def test_topics(self, publisher, fields, expected, plain_console_test_logger_on_trace):
        publisher.return_value.list_topics.return_value = []
        action = PubSubStageTopicsAction(method='TOPICS', project='p', **fields)

        action.execute(logger=plain_console_test_logger_on_trace, context=Context())

        assert publisher.return_value.list_topics.call_args.kwargs['timeout'] == expected

    @pytest.mark.parametrize('fields, expected', [({}, DEFAULT_TIMEOUT), ({'timeout': 4}, 4)])
    @patch('folker.module.gcp.pubsub.action.SubscriberClient')
    def test_subscriptions(self, subscriber, fields, expected,
                           plain_console_test_logger_on_trace):
        subscriber.return_value.list_subscriptions.return_value = []
        action = PubSubStageSubscriptionsAction(method='SUBSCRIPTIONS', project='p', **fields)

        action.execute(logger=plain_console_test_logger_on_trace, context=Context())

        assert subscriber.return_value.list_subscriptions.call_args.kwargs['timeout'] == expected

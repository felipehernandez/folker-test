from unittest.mock import patch

import pytest
from kazoo.exceptions import NodeExistsError, NoNodeError

from folker.logger import TestLogger
from folker.model import Context
from folker.module.zookeeper.action import (ZookeeperStageCreateAction, ZookeeperStageDeleteAction,
                                            ZookeeperStageExistsAction, ZookeeperStageGetAction,
                                            ZookeeperStageSetAction)

KAZOO = 'folker.module.zookeeper.action.KazooClient'


@pytest.fixture
def logger(mocker):
    return mocker.Mock(spec=TestLogger)


@pytest.fixture
def client():
    with patch(KAZOO) as kazoo:
        yield kazoo.return_value


def run(cls, logger, context=None, **fields):
    return cls(host='zk:2181', node='/the/node', **fields) \
        .execute(logger=logger, context=context or Context())


@pytest.mark.action_zookeeper
class TestZookeeperExists:
    def test_an_existing_node_saves_its_path(self, client, logger):
        client.exists.return_value = object()

        context = run(ZookeeperStageExistsAction, logger)

        assert context.stage_variables['path'] == '/the/node'
        client.exists.assert_called_once_with('/the/node')

    def test_a_missing_node_saves_none(self, client, logger):
        client.exists.return_value = None

        assert run(ZookeeperStageExistsAction, logger).stage_variables['path'] is None

    def test_it_connects_to_the_host_and_stops_the_client(self, logger):
        with patch(KAZOO) as kazoo:
            run(ZookeeperStageExistsAction, logger)

        kazoo.assert_called_once_with(hosts='zk:2181')
        kazoo.return_value.start.assert_called_once()
        kazoo.return_value.stop.assert_called_once()


@pytest.mark.action_zookeeper
class TestZookeeperCreate:
    def test_a_node_without_data(self, client, logger):
        client.create.return_value = '/the/node'

        context = run(ZookeeperStageCreateAction, logger)

        assert context.stage_variables['path'] == '/the/node'
        kwargs = client.create.call_args.kwargs
        assert (kwargs['path'], kwargs['value'], kwargs['makepath'], kwargs['ephemeral'],
                kwargs['include_data']) == ('/the/node', b'', True, False, False)

    def test_a_node_with_data_saves_the_path_and_the_stats(self, client, logger):
        client.create.return_value = ('/the/node', 'the-stats')

        context = run(ZookeeperStageCreateAction, logger, data='payload')

        assert context.stage_variables['path'] == '/the/node'
        assert context.stage_variables['stats'] == 'the-stats'
        kwargs = client.create.call_args.kwargs
        assert kwargs['value'] == b'payload' and kwargs['include_data'] is True

    def test_an_ephemeral_node(self, client, logger):
        client.create.return_value = '/the/node'

        run(ZookeeperStageCreateAction, logger, ephemeral=True)

        assert client.create.call_args.kwargs['ephemeral'] is True

    def test_variables_are_resolved(self, client, logger):
        client.create.return_value = '/the/node'

        run(ZookeeperStageCreateAction, logger, data='hello ${who}',
            context=Context(test_variables={'who': 'folker'}))

        assert client.create.call_args.kwargs['value'] == b'hello folker'

    def test_an_existing_node_is_reported_without_failing_the_action(self, client, logger):
        client.create.side_effect = NodeExistsError()

        context = run(ZookeeperStageCreateAction, logger)

        assert 'error' in context.stage_variables
        assert 'path' not in context.stage_variables
        client.stop.assert_called_once()


@pytest.mark.action_zookeeper
class TestZookeeperGet:
    def test_the_data_is_decoded_and_saved_with_the_stats(self, client, logger):
        client.get.return_value = (b'the data', 'the-stats')

        context = run(ZookeeperStageGetAction, logger)

        assert context.stage_variables['data'] == 'the data'
        assert context.stage_variables['stats'] == 'the-stats'
        client.get.assert_called_once_with('/the/node')
        client.stop.assert_called_once()

    def test_a_node_without_data_saves_an_empty_string(self, client, logger):
        client.get.return_value = (b'', 'the-stats')

        assert run(ZookeeperStageGetAction, logger).stage_variables['data'] == ''


@pytest.mark.action_zookeeper
class TestZookeeperSet:
    def test_the_value_is_written_and_the_stats_saved(self, client, logger):
        client.set.return_value = 'the-stats'

        context = run(ZookeeperStageSetAction, logger, data='new value')

        assert context.stage_variables['stats'] == 'the-stats'
        assert client.set.call_args.kwargs['path'] == '/the/node'
        assert client.set.call_args.kwargs['value'] == b'new value'
        client.stop.assert_called_once()

    def test_without_a_version_any_version_is_overwritten(self, client, logger):
        run(ZookeeperStageSetAction, logger, data='x')

        assert client.set.call_args.kwargs['version'] == -1

    def test_a_version_makes_the_write_conditional(self, client, logger):
        run(ZookeeperStageSetAction, logger, data='x', version=3)

        assert client.set.call_args.kwargs['version'] == 3


@pytest.mark.action_zookeeper
class TestZookeeperDelete:
    def test_the_node_is_deleted(self, client, logger):
        run(ZookeeperStageDeleteAction, logger)

        client.delete.assert_called_once_with('/the/node')
        client.stop.assert_called_once()


@pytest.mark.action_zookeeper
class TestZookeeperFailures:
    """Only `create` catches errors. The others raise, which fails the test through the stage:
    that is today's behaviour, and the client is left open when they do (BUG-23)"""

    @pytest.mark.parametrize('cls, operation, fields', [
        (ZookeeperStageGetAction, 'get', {}),
        (ZookeeperStageDeleteAction, 'delete', {}),
        (ZookeeperStageSetAction, 'set', {'data': 'x'}),
        (ZookeeperStageExistsAction, 'exists', {}),
    ], ids=['get', 'delete', 'set', 'exists'])
    def test_an_error_raises(self, client, logger, cls, operation, fields):
        getattr(client, operation).side_effect = NoNodeError()

        with pytest.raises(NoNodeError):
            run(cls, logger, **fields)

    @pytest.mark.xfail(strict=True, reason='BUG-23: the client is not stopped when the operation '
                                           'raises, so its connection thread is left running')
    @pytest.mark.parametrize('cls, operation, fields', [
        (ZookeeperStageGetAction, 'get', {}),
        (ZookeeperStageDeleteAction, 'delete', {}),
        (ZookeeperStageSetAction, 'set', {'data': 'x'}),
        (ZookeeperStageExistsAction, 'exists', {}),
    ], ids=['get', 'delete', 'set', 'exists'])
    def test_the_client_is_stopped_when_the_operation_raises(self, client, logger, cls,
                                                             operation, fields):
        getattr(client, operation).side_effect = NoNodeError()

        with pytest.raises(NoNodeError):
            run(cls, logger, **fields)

        client.stop.assert_called_once()

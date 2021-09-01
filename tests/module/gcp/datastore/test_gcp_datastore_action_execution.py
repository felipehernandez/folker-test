from unittest.mock import Mock, call

import pytest

from folker.model import Context
from folker.module.gcp.datastore.action import DatastoreStageAction


@pytest.mark.action_gcp_datastore
def test_gcp_datastore_put(mocker):
    entity_data = {}
    action = DatastoreStageAction(method='PUT',
                                  host='aHost',
                                  project='aProject',
                                  key={'id': 'KEY_ID', 'kind': 'KEY_KIND'},
                                  entity=entity_data)

    mocked_logger = mocker.patch('folker.logger.TestLogger')

    datastore_client = mocker.patch('folker.module.gcp.datastore.action.Client', name='Client')
    datastore_client.return_value = datastore_client
    datastore_client.key.return_value = 'ITEM_KEY'
    datastore_client.put.return_value = None
    entity = mocker.patch('folker.module.gcp.datastore.action.Entity', name='Entity')
    entity.return_value = entity
    entity.update.return_value = None

    action.execute(logger=mocked_logger, context=Context())

    datastore_client.key.assert_called_with('KEY_KIND', 'KEY_ID')
    entity.assert_called_with(key='ITEM_KEY')
    entity.update.assert_called_with(entity_data)
    datastore_client.put.assert_called_with(entity)


@pytest.mark.action_gcp_datastore
def test_gcp_datastore_get_existing(mocker):
    action = DatastoreStageAction(method='GET',
                                  host='aHost',
                                  project='aProject',
                                  key={'id': 'KEY_ID', 'kind': 'KEY_KIND'})

    mocked_logger = mocker.patch('folker.logger.TestLogger')

    datastore_client = mocker.patch('folker.module.gcp.datastore.action.Client', name='Client')
    datastore_client.return_value = datastore_client
    datastore_client.key.return_value = 'ITEM_KEY'
    entity = mocker.patch('folker.module.gcp.datastore.action.Entity', name='Entity')
    datastore_client.get.return_value = entity
    entity.key.kind = 'KEY_KIND'
    entity.key.id = 'KEY_ID'
    entity.key.name = 'KEY_NAME'
    entity.copy.return_value = {'entity': 'value'}

    result_context = action.execute(logger=mocked_logger, context=Context())

    datastore_client.key.assert_called_with('KEY_KIND', 'KEY_ID')
    datastore_client.get.assert_called_with('ITEM_KEY')
    assert result_context.stage_variables.get('key') == {'kind': 'KEY_KIND',
                                                         'id': 'KEY_ID',
                                                         'name': 'KEY_NAME'}
    assert result_context.stage_variables.get('entity') == {'entity': 'value'}


@pytest.mark.action_gcp_datastore
def test_gcp_datastore_get_not_existing(mocker):
    action = DatastoreStageAction(method='GET',
                                  host='aHost',
                                  project='aProject',
                                  key={'id': 'KEY_ID', 'kind': 'KEY_KIND'})

    mocked_logger = mocker.patch('folker.logger.TestLogger')

    datastore_client = mocker.patch('folker.module.gcp.datastore.action.Client', name='Client')
    datastore_client.return_value = datastore_client
    datastore_client.key.return_value = 'ITEM_KEY'
    datastore_client.get.return_value = None

    result_context = action.execute(logger=mocked_logger, context=Context())

    datastore_client.key.assert_called_with('KEY_KIND', 'KEY_ID')
    datastore_client.get.assert_called_with('ITEM_KEY')
    assert result_context.stage_variables.get('key') is None
    assert result_context.stage_variables.get('entity') is None


@pytest.mark.action_gcp_datastore
def test_gcp_datastore_delete(mocker):
    action = DatastoreStageAction(method='DELETE',
                                  host='aHost',
                                  project='aProject',
                                  key={'id': 'KEY_ID', 'kind': 'KEY_KIND'})

    mocked_logger = mocker.patch('folker.logger.TestLogger')

    datastore_client = mocker.patch('folker.module.gcp.datastore.action.Client', name='Client')
    datastore_client.return_value = datastore_client
    datastore_client.key.return_value = 'ITEM_KEY'
    datastore_client.delete.return_value = None

    action.execute(logger=mocked_logger, context=Context())

    datastore_client.key.assert_called_with('KEY_KIND', 'KEY_ID')
    datastore_client.delete.assert_called_with('ITEM_KEY')


@pytest.mark.action_gcp_datastore
def test_gcp_datastore_query(mocker):
    action = DatastoreStageAction(method='QUERY',
                                  host='aHost',
                                  project='aProject',
                                  key={'kind': 'KEY_KIND'})

    mocked_logger = mocker.patch('folker.logger.TestLogger')

    datastore_client = mocker.patch('folker.module.gcp.datastore.action.Client', name='Client')
    datastore_client.return_value = datastore_client
    query_result = Mock()
    datastore_client.query.return_value = query_result
    query_result.fetch.return_value = ['entity1', 'entity2']

    result_context = action.execute(logger=mocked_logger, context=Context())

    assert result_context.stage_variables.get('result') == ['entity1', 'entity2']


@pytest.mark.action_gcp_datastore
def test_gcp_datastore_bulkdelete(mocker):
    action = DatastoreStageAction(method='BULK_DELETE',
                                  host='aHost',
                                  project='aProject',
                                  key={'kind': 'KEY_KIND', 'ids': ['id1', 'id2']})

    mocked_logger = mocker.patch('folker.logger.TestLogger')

    datastore_client = mocker.patch('folker.module.gcp.datastore.action.Client', name='Client')
    datastore_client.return_value = datastore_client
    datastore_client.key.side_effect = ['ITEM_KEY_1', 'ITEM_KEY_2']

    action.execute(logger=mocked_logger, context=Context())

    datastore_client.key.assert_has_calls([call('KEY_KIND', 'id1'),
                                           call('KEY_KIND', 'id2')])
    datastore_client.delete_multi.assert_called_with(['ITEM_KEY_1', 'ITEM_KEY_2'])

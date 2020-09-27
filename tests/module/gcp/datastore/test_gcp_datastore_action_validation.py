from pytest import raises

from folker.model.error import InvalidSchemaDefinitionException
from folker.module.gcp.datastore.action import DatastoreStageAction


def test_action_gcp_datastore_validate_missing_method():
    with raises(InvalidSchemaDefinitionException) as raised_exception:
        DatastoreStageAction()

    assert 'action.method' in raised_exception.value.details['wrong_fields']


def test_action_gcp_datastore_validate_wrong_method():
    with raises(InvalidSchemaDefinitionException) as raised_exception:
        DatastoreStageAction(method='X')

    assert 'action.method' in raised_exception.value.details['wrong_fields']


def test_action_gcp_datastore_validate_missing_project():
    action = DatastoreStageAction(method='PUT')

    with raises(InvalidSchemaDefinitionException) as raised_exception:
        action.validate()

    assert 'action.project' in raised_exception.value.details['missing_fields']


def test_action_gcp_datastore_validate_missing_key():
    action = DatastoreStageAction(method='PUT')

    with raises(InvalidSchemaDefinitionException) as raised_exception:
        action.validate()

    assert 'action.key' in raised_exception.value.details['missing_fields']


def test_action_gcp_datastore_validate_missing_key_kind_on_get():
    action = DatastoreStageAction(method='GET', key={})

    with raises(InvalidSchemaDefinitionException) as raised_exception:
        action.validate()

    assert 'action.key.kind' in raised_exception.value.details['missing_fields']


def test_action_gcp_datastore_validate_missing_key_id_and_name_on_get():
    action = DatastoreStageAction(method='GET', key={'kind': 'a_kind'})

    with raises(InvalidSchemaDefinitionException) as raised_exception:
        action.validate()

    assert 'action.key.id' in raised_exception.value.details['missing_fields']
    assert 'action.key.name' in raised_exception.value.details['missing_fields']


def test_action_gcp_datastore_validate_missing_key_kind_on_put():
    action = DatastoreStageAction(method='PUT', key={})

    with raises(InvalidSchemaDefinitionException) as raised_exception:
        action.validate()

    assert 'action.key.kind' in raised_exception.value.details['missing_fields']


def test_action_gcp_datastore_validate_missing_key_id_and_name_on_put():
    action = DatastoreStageAction(method='PUT', key={'kind': 'a_kind'})

    with raises(InvalidSchemaDefinitionException) as raised_exception:
        action.validate()

    assert 'action.key.id' in raised_exception.value.details['missing_fields']
    assert 'action.key.name' in raised_exception.value.details['missing_fields']


def test_action_gcp_datastore_validate_missing_key_kind_on_delete():
    action = DatastoreStageAction(method='DELETE', key={})

    with raises(InvalidSchemaDefinitionException) as raised_exception:
        action.validate()

    assert 'action.key.kind' in raised_exception.value.details['missing_fields']


def test_action_gcp_datastore_validate_missing_key_id_and_name_on_delete():
    action = DatastoreStageAction(method='DELETE', key={'kind': 'a_kind'})

    with raises(InvalidSchemaDefinitionException) as raised_exception:
        action.validate()

    assert 'action.key.id' in raised_exception.value.details['missing_fields']
    assert 'action.key.name' in raised_exception.value.details['missing_fields']


def test_action_gcp_datastore_validate_complete_get_with_id():
    action = DatastoreStageAction(method='GET',
                                  project='a_project',
                                  key={'kind': 'a_kind', 'id': 'an_id'})

    action.validate()

    assert True


def test_action_gcp_datastore_validate_complete_get_with_name():
    action = DatastoreStageAction(method='GET',
                                  project='a_project',
                                  key={'kind': 'a_kind', 'name': 'a_name'})

    action.validate()

    assert True


def test_action_gcp_datastore_validate_complete_delete_with_id():
    action = DatastoreStageAction(method='DELETE',
                                  project='a_project',
                                  key={'kind': 'a_kind', 'id': 'an_id'})

    action.validate()

    assert True


def test_action_gcp_datastore_validate_complete_delete_with_name():
    action = DatastoreStageAction(method='DELETE',
                                  project='a_project',
                                  key={'kind': 'a_kind', 'name': 'a_name'})

    action.validate()

    assert True


def test_action_gcp_datastore_validate_complete_put_with_id():
    action = DatastoreStageAction(method='PUT',
                                  project='a_project',
                                  key={'kind': 'a_kind', 'id': 'an_id'},
                                  entity={'key': 'value'})

    action.validate()

    assert True


def test_action_gcp_datastore_validate_complete_put_with_name():
    action = DatastoreStageAction(method='PUT',
                                  project='a_project',
                                  key={'kind': 'a_kind', 'name': 'a_name'},
                                  entity={'key': 'value'})

    action.validate()

    assert True


def test_action_gcp_datastore_validate_missing_entity_on_put():
    action = DatastoreStageAction(method='PUT', key={})

    with raises(InvalidSchemaDefinitionException) as raised_exception:
        action.validate()

    assert 'action.entity' in raised_exception.value.details['missing_fields']

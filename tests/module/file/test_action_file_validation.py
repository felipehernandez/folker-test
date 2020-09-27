from pytest import raises

from folker.model.error import InvalidSchemaDefinitionException
from folker.module.file.action import FileStageAction


def test_action_file_validate_missing_method():
    with raises(InvalidSchemaDefinitionException) as raised_exception:
        FileStageAction()

    assert 'action.method' in raised_exception.value.details['wrong_fields']


def test_action_file_validate_wrong_method():
    with raises(InvalidSchemaDefinitionException) as raised_exception:
        FileStageAction(method='X')

    assert 'action.method' in raised_exception.value.details['wrong_fields']


def test_action_file_validate_missing_file():
    action = FileStageAction(method='READ')

    with raises(InvalidSchemaDefinitionException) as raised_exception:
        action.validate()

    assert 'action.file' in raised_exception.value.details['missing_fields']


def test_action_file_validate_missing_content_on_read():
    action = FileStageAction(method='READ', file='a_file')

    action.validate()

    assert True


def test_action_file_validate_missing_content_on_write():
    action = FileStageAction(method='WRITE', file='a_file')

    with raises(InvalidSchemaDefinitionException) as raised_exception:
        action.validate()

    assert 'action.content' in raised_exception.value.details['missing_fields']

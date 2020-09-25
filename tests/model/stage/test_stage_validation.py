import pytest

from folker.model import Stage
from folker.model.error import InvalidSchemaDefinitionException


def test_stage_validation_named_missing_action():
    stage = Stage(name='StageName')

    with pytest.raises(InvalidSchemaDefinitionException) as raised_exception:
        stage.validate()

        assert raised_exception.wrong_fields == ['StageName[name].action']


def test_stage_validation_ided_missing_action():
    stage = Stage(id='StageId')

    with pytest.raises(InvalidSchemaDefinitionException) as raised_exception:
        stage.validate()

        assert raised_exception.wrong_fields == ['StageId[id].action']


def test_stage_validation_invalid_action(mocker):
    mocked_action = mocker.patch('folker.model.stage.StageAction')

    stage = Stage(name='StageName', action=mocked_action)

    mocked_action.validate.side_effect = InvalidSchemaDefinitionException(missing_fields=['field'])

    with pytest.raises(InvalidSchemaDefinitionException) as raised_exception:
        stage.validate()

        assert raised_exception.missing_fields == ['field']


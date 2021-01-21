import pytest

from folker.model import Test
from folker.model.error import InvalidSchemaDefinitionException


def test_test_validation_missing_name():
    test = Test()

    with pytest.raises(InvalidSchemaDefinitionException) as raise_exception:
        test.validate()

    assert raise_exception.value.details['missing_fields'] == ['test.name']


def test_test_validation_stage_validation_error(mocker):
    mocked_stage = mocker.patch('folker.model.stage.Stage')

    test = Test(name='TestName', stages=[mocked_stage])

    mocked_stage.validate.side_effect = InvalidSchemaDefinitionException(wrong_fields=['field'])

    with pytest.raises(InvalidSchemaDefinitionException) as raise_exception:
        test.validate()

    assert raise_exception.value.details['wrong_fields'] == ['TestName.field']


def test_test_validation_stage_valid(mocker):
    mocked_stage = mocker.patch('folker.model.stage.Stage')

    test = Test(name="TestName", stages=[mocked_stage])

    mocked_stage.validate.return_value = None

    test.validate()

    assert True

from folker.model import Test
from folker.model.validation import ValidationReport


def test_test_validation_missing_name():
    test = Test()

    assert not test
    assert not test.validation_report
    assert 'test.name' in test.validation_report.missing_fields


def test_test_validation_stage_validation_error(mocker):
    mocked_stage = mocker.patch('folker.model.stage.Stage')

    test = Test(name='TestName', stages=[mocked_stage])

    mocked_stage.__bool__.return_value = False
    mocked_stage.validation_report = ValidationReport(missing_fields={'a_missing_field'})

    assert not test
    assert not test.validation_report
    assert 'test.TestName.a_missing_field' in test.validation_report.missing_fields


def test_test_validation_stage_valid(mocker):
    mocked_stage = mocker.patch('folker.model.stage.Stage')

    test = Test(name="TestName", stages=[mocked_stage])

    mocked_stage.__bool__.return_value = True

    assert test
    assert test.validation_report

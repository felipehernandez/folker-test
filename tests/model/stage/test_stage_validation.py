from folker.model import Stage
from folker.module.void.action import VoidStageAction
from folker.module.wait.action import WaitStageAction


class TestStageValidation:
    def test_validate_no_name_nor_id(self):
        stage = Stage(action=VoidStageAction())

        assert not stage
        assert not stage.validation_report
        assert 'stage.name' in stage.validation_report.missing_fields
        assert 'stage.id' in stage.validation_report.missing_fields

    def test_validate_correct(self):
        stage = Stage(name='a_name',
                      action=VoidStageAction())

        assert stage
        assert stage.validation_report

    def test_validate_incorrect_action(self):
        stage = Stage(name='a_name',
                      action=WaitStageAction())

        assert not stage
        assert not stage.validation_report
        assert 'stage.a_name.action.time' in stage.validation_report.missing_fields

    def test_validate_incorrect_action_no_name(self):
        stage = Stage(action=WaitStageAction())

        assert not stage
        assert not stage.validation_report
        assert 'stage.name' in stage.validation_report.missing_fields
        assert 'stage.id' in stage.validation_report.missing_fields
        assert 'stage.None.action.time' in stage.validation_report.missing_fields

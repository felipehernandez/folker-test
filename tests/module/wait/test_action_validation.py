from folker.module.wait.action import WaitStageAction


class TestWaitActionValidation:
    def test_validate_empty(self):
        action = WaitStageAction()

        assert not action
        assert not action.validation_report
        assert 'action.time' in action.validation_report.missing_fields

    def test_validate_correct(self):
        action = WaitStageAction(time=3)

        assert action
        assert action.validation_report

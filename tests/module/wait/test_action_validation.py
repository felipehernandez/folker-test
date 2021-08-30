import pytest

from folker.module.wait.action import WaitStageAction


@pytest.mark.action_correctness
@pytest.mark.action_wait
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

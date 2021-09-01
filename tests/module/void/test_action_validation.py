import pytest

from folker.module.void.action import VoidStageAction


@pytest.mark.action_correctness
@pytest.mark.action_void
class TestVoidActionValidation:
    def test_validate_empty(self):
        action = VoidStageAction()

        assert action

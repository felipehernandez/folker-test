from folker.module.void.action import VoidStageAction


class TestVoidActionValidation:
    def test_validate_empty(self):
        action = VoidStageAction()

        assert action

import pytest

from folker.module.void.action import VoidStageAction


class TestVoidAction:
    action: VoidStageAction

    @pytest.fixture(autouse=True)
    def setup(self):
        self.action = VoidStageAction()
        yield

    def test_validate(self):
        # Should not throw any exception
        self.action.validate()

import pytest

from folker.module.void.action import VoidAction


class TestVoidAction:
    action: VoidAction

    @pytest.fixture(autouse=True)
    def setup(self):
        self.action = VoidAction()
        yield

    def test_validate(self):
        # Should not throw any exception
        self.action.validate()

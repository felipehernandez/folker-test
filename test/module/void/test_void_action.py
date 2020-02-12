from unittest import TestCase

from folker.module.void.action import VoidAction


class TestVoidAction(TestCase):
    action: VoidAction

    def setUp(self) -> None:
        self.action = VoidAction()

    def test_validate(self):
        # Should not throw any exception
        self.action.validate()

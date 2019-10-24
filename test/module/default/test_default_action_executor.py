from unittest import TestCase

from folker.module.default.action_executor import DefaultActionExecutor


class TestDefaultActionExecutor(TestCase):

    def test_execution(self):
        executor = DefaultActionExecutor()

        test_context, stage_context = executor.execute(None, {}, {})

        self.assertEqual({}, test_context)
        self.assertEqual({}, stage_context)

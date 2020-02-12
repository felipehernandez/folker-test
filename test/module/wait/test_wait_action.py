from unittest import TestCase
from unittest.mock import Mock

from folker.model.error.load import InvalidSchemaDefinitionException
from folker.module.wait.action import WaitAction


class TestWaitAction(TestCase):
    action: WaitAction

    def setUp(self) -> None:
        self.action = WaitAction()

    def test_validate_missing_time(self):
        with self.assertRaises(InvalidSchemaDefinitionException) as execution_context:
            self.action.validate()

        self.assertTrue('action.time' in execution_context.exception.details['missing_fields'])

    def test_validate_correct(self):
        self.action.time = 3

        self.action.validate()

    def test_execution(self):
        logger = Mock()

        self.action.time = 0.1

        test_context, stage_context = self.action.execute(logger, {}, {})

        self.assertEqual({}, test_context)
        self.assertTrue('elapsed_time' in stage_context)
        self.assertTrue(stage_context['elapsed_time'] >= 100)

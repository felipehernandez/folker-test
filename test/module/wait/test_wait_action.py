from unittest import TestCase
from unittest.mock import Mock

from folker.model.context import Context
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

        context = self.action.execute(logger, context=Context())

        self.assertEqual({}, context.test_variables)
        self.assertTrue('elapsed_time' in context.stage_variables)
        self.assertTrue(context.stage_variables['elapsed_time'] >= 100)

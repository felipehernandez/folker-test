from unittest import TestCase
from unittest.mock import Mock

from folker.model.error.load import InvalidSchemaDefinitionException
from folker.module.printt.action import PrintAction


class TestVoidAction(TestCase):
    action: PrintAction

    def setUp(self) -> None:
        self.action = PrintAction()

    def test_validate_missing_message(self):
        with self.assertRaises(InvalidSchemaDefinitionException) as execution_context:
            self.action.validate()

        self.assertTrue('action.message' in execution_context.exception.details['missing_fields'])

    def test_validate_correct(self):
        self.action.message = 'a_message'

        self.action.validate()

    def test_execution(self):
        logger = Mock()

        self.action.message = 'Hello world'

        test_context, stage_context = self.action.execute(logger, {}, {})

        self.assertEqual({}, test_context)
        self.assertTrue('elapsed_time' in stage_context)
        logger.message.assert_called_with('Hello world')

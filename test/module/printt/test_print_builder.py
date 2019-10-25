from unittest import TestCase

from folker.model.error.load import InvalidSchemaDefinitionException
from folker.module.printt.builder import PrintStageBuilder


class TestVoidStageBuilder(TestCase):

    def test_given_print_stage_then_recognise(self):
        builder = PrintStageBuilder()

        stage_definition = {
            'type': 'PRINT'
        }

        recognises = builder.recognises(stage_definition)

        self.assertTrue(recognises)

    def test_given_not_print_stage_then_recognise(self):
        builder = PrintStageBuilder()

        stage_definition = {
            'type': 'OTHER'
        }

        recognises = builder.recognises(stage_definition)

        self.assertFalse(recognises)

    def test_given_valid_print_stage_then_build(self):
        builder = PrintStageBuilder()

        stage_definition = {
            'id': '1',
            'name': 'print_stage',
            'type': 'PRINT',
            'action':
                {'message': 'Hello world'}
        }

        stage = builder.build(stage_definition)

        self.assertIsNotNone(stage)
        self.assertIsNotNone(stage.data)
        self.assertIsNotNone(stage.executors)
        self.assertIsNotNone(stage.executors.action)
        self.assertIsNotNone(stage.executors.assertion)
        self.assertIsNotNone(stage.executors.save)
        self.assertIsNotNone(stage.executors.log)

    def test_given_valid_print_stage_with_missing_action_then_exception(self):
        builder = PrintStageBuilder()

        stage_definition = {
            'id': '1',
            'name': 'print_stage',
            'type': 'PRINT'
        }

        try:
            builder.build(stage_definition)
        except InvalidSchemaDefinitionException as e:
            self.assertEqual(['action'], e.details['missing_fields'])

    def test_given_valid_print_stage_with_missing_message_in_action__then_exception(self):
        builder = PrintStageBuilder()

        stage_definition = {
            'id': '1',
            'name': 'print_stage',
            'type': 'PRINT',
            'action': {}
        }

        try:
            builder.build(stage_definition)
        except InvalidSchemaDefinitionException as e:
            self.assertEqual(['action.message'], e.details['missing_fields'])

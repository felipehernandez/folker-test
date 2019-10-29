from unittest import TestCase

from folker.model.error.load import InvalidSchemaDefinitionException
from folker.module.rest.action_executor import RestActionExecutor
from folker.module.rest.builder import RestStageBuilder


class TestRestStageBuilder(TestCase):

    def test_given_rest_stage_then_recognise(self):
        builder = RestStageBuilder()

        stage_definition = {
            'type': 'REST'
        }

        recognises = builder.recognises(stage_definition)

        self.assertTrue(recognises)

    def test_given_not_rest_stage_then_recognise(self):
        builder = RestStageBuilder()

        stage_definition = {
            'type': 'OTHER'
        }

        recognises = builder.recognises(stage_definition)

        self.assertFalse(recognises)

    def test_given_valid_rest_stage_then_build(self):
        builder = RestStageBuilder()

        stage_definition = {
            'name': 'rest_stage',
            'type': 'REST',
            'action':
                {
                    'method': 'GET',
                    'host': 'http://localhost:8080'
                }
        }

        stage = builder.build_stage(stage_definition)

        self.assertIsNotNone(stage)
        self.assertIsNotNone(stage.data)
        self.assertIsNotNone(stage.executors)
        self.assertIsNotNone(stage.executors.action)
        self.assertEqual(RestActionExecutor, type(stage.executors.action))
        self.assertIsNotNone(stage.executors.assertion)
        self.assertIsNotNone(stage.executors.save)
        self.assertIsNotNone(stage.executors.log)

    def test_given_valid_rest_stage_with_missing_action_then_exception(self):
        builder = RestStageBuilder()

        stage_definition = {
            'name': 'rest_stage',
            'type': 'REST'
        }

        try:
            builder.build_stage(stage_definition)
            raise AssertionError('Should not get here')
        except InvalidSchemaDefinitionException as e:
            self.assertEqual(['action'], e.details['missing_fields'])

    def test_given_valid_rest_stage_with_missing_host_in_action_then_exception(self):
        builder = RestStageBuilder()

        stage_definition = {
            'name': 'rest_stage',
            'type': 'REST',
            'action':
                {
                    'method': 'GET'
                }
        }

        try:
            builder.build_stage(stage_definition)
            raise AssertionError('Should not get here')
        except InvalidSchemaDefinitionException as e:
            self.assertEqual(['action.host'], e.details['missing_fields'])

    def test_given_valid_rest_stage_with_missing_method_in_action_then_exception(self):
        builder = RestStageBuilder()

        stage_definition = {
            'name': 'rest_stage',
            'type': 'REST',
            'action':
                {
                    'host': 'http://localhost:8080'
                }
        }

        try:
            builder.build_stage(stage_definition)
            raise AssertionError('Should not get here')
        except InvalidSchemaDefinitionException as e:
            self.assertEqual(['action.method'], e.details['missing_fields'])

    def test_given_valid_rest_stage_with_wrong_method_in_action_then_exception(self):
        builder = RestStageBuilder()

        stage_definition = {
            'name': 'rest_stage',
            'type': 'REST',
            'action':
                {
                    'method': 'OTHER',
                    'host': 'http://localhost:8080'
                }
        }

        try:
            builder.build_stage(stage_definition)
            raise AssertionError('Should not get here')
        except InvalidSchemaDefinitionException as e:
            self.assertEqual(['action.method'], e.details['wrong_fields'])

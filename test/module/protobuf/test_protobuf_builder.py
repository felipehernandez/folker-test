from unittest import TestCase

from folker.model.error.load import InvalidSchemaDefinitionException
from folker.module.protobuf import ProtobufStageBuilder
from folker.module.protobuf.action_executor import ProtobufActionExecutor


class TestProtobufStageBuilder(TestCase):

    def test_given_protobuf_stage_then_recognise(self):
        builder = ProtobufStageBuilder()

        stage_definition = {
            'type': 'PROTOBUF'
        }

        recognises = builder.recognises(stage_definition)

        self.assertTrue(recognises)

    def test_given_not_protobuf_stage_then_recognise(self):
        builder = ProtobufStageBuilder()

        stage_definition = {
            'type': 'OTHER'
        }

        recognises = builder.recognises(stage_definition)

        self.assertFalse(recognises)

    def test_given_valid_protobuf_stage_then_build(self):
        builder = ProtobufStageBuilder()

        stage_definition = {
            'name': 'protobuf_stage',
            'type': 'PROTOBUF',
            'action':
                {
                    'method': 'WRITE',
                    'package': 'a_protobuf_package',
                    'clazz': 'AClass',
                    'data':
                        {'attribute_1': 'value_1'}
                }
        }

        stage = builder.build_stage(stage_definition)

        self.assertIsNotNone(stage)
        self.assertIsNotNone(stage.data)
        self.assertIsNotNone(stage.executors)
        self.assertIsNotNone(stage.executors.action)
        self.assertEqual(ProtobufActionExecutor, type(stage.executors.action))
        self.assertIsNotNone(stage.executors.assertion)
        self.assertIsNotNone(stage.executors.save)
        self.assertIsNotNone(stage.executors.log)

    def test_given_valid_protobuf_stage_with_missing_action_then_exception(self):
        builder = ProtobufStageBuilder()

        stage_definition = {
            'name': 'protobuf_stage',
            'type': 'PROTOBUF'
        }

        try:
            builder.build_stage(stage_definition)
            raise AssertionError('Should not get here')
        except InvalidSchemaDefinitionException as e:
            self.assertEqual(['action'], e.details['missing_fields'])

    def test_given_valid_protobuf_stage_with_missing_package_in_action_then_exception(self):
        builder = ProtobufStageBuilder()

        stage_definition = {
            'name': 'protobuf_stage',
            'type': 'REST',
            'action':
                {
                    'method': 'WRITE',
                    'clazz': 'AClass',
                    'data':
                        {'attribute_1': 'value_1'}
                }
        }

        try:
            builder.build_stage(stage_definition)
            raise AssertionError('Should not get here')
        except InvalidSchemaDefinitionException as e:
            self.assertEqual(['action.package'], e.details['missing_fields'])

    def test_given_valid_protobuf_stage_with_missing_method_in_action_then_exception(self):
        builder = ProtobufStageBuilder()

        stage_definition = {
            'name': 'protobuf_stage',
            'type': 'REST',
            'action':
                {
                    'package': 'a_protobuf_package',
                    'clazz': 'AClass',
                    'data':
                        {'attribute_1': 'value_1'}
                }
        }

        try:
            builder.build_stage(stage_definition)
            raise AssertionError('Should not get here')
        except InvalidSchemaDefinitionException as e:
            self.assertEqual(['action.method'], e.details['missing_fields'])

    def test_given_valid_protobuf_stage_with_missing_clazz_in_action_then_exception(self):
        builder = ProtobufStageBuilder()

        stage_definition = {
            'name': 'protobuf_stage',
            'type': 'REST',
            'action':
                {
                    'method': 'WRITE',
                    'package': 'a_protobuf_package',
                    'data':
                        {'attribute_1': 'value_1'}
                }
        }

        try:
            builder.build_stage(stage_definition)
            raise AssertionError('Should not get here')
        except InvalidSchemaDefinitionException as e:
            self.assertEqual(['action.class'], e.details['missing_fields'])

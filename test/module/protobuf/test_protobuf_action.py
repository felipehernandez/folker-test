from unittest import TestCase

from folker.model.error.load import InvalidSchemaDefinitionException
from folker.module.protobuf.action import ProtobufAction, ProtobufMethod


class TestProtobufAction(TestCase):
    action: ProtobufAction

    def setUp(self) -> None:
        self.action = ProtobufAction()

    def test_validate_correct_create(self):
        self.action.method = ProtobufMethod.CREATE
        self.action.package = 'a_protobuf_package'
        self.action.clazz = 'AClass'
        self.action.data = {'attribute_1': 'value_1'}

        self.action.validate()

    def test_validate_correct_load(self):
        self.action.method = ProtobufMethod.LOAD
        self.action.package = 'a_protobuf_package'
        self.action.clazz = 'AClass'
        self.action.message = 'a_message'

        self.action.validate()

    def test_validate_missing_attribute_method(self):
        self.action.package = 'a_protobuf_package'
        self.action.clazz = 'AClass'
        self.action.data = {'attribute_1': 'value_1'}

        with self.assertRaises(InvalidSchemaDefinitionException) as execution_context:
            self.action.validate()

        self.assertTrue('action.method' in execution_context.exception.details['missing_fields'])

    def test_validate_missing_attribute_package(self):
        self.action.method = ProtobufMethod.CREATE
        self.action.clazz = 'AClass'
        self.action.data = {'attribute_1': 'value_1'}

        with self.assertRaises(InvalidSchemaDefinitionException) as execution_context:
            self.action.validate()

        self.assertTrue('action.package' in execution_context.exception.details['missing_fields'])

    def test_validate_missing_attribute_class(self):
        self.action.method = ProtobufMethod.CREATE
        self.action.package = 'a_protobuf_package'
        self.action.data = {'attribute_1': 'value_1'}

        with self.assertRaises(InvalidSchemaDefinitionException) as execution_context:
            self.action.validate()

        self.assertTrue('action.class' in execution_context.exception.details['missing_fields'])

    def test_validate_missing_attribute_data(self):
        self.action.method = ProtobufMethod.CREATE
        self.action.package = 'a_protobuf_package'
        self.action.clazz = 'AClass'

        with self.assertRaises(InvalidSchemaDefinitionException) as execution_context:
            self.action.validate()

        self.assertTrue('action.data' in execution_context.exception.details['missing_fields'])

    def test_validate_missing_attribute_message(self):
        self.action.method = ProtobufMethod.LOAD
        self.action.package = 'a_protobuf_package'
        self.action.clazz = 'AClass'

        with self.assertRaises(InvalidSchemaDefinitionException) as execution_context:
            self.action.validate()

        self.assertTrue('action.message' in execution_context.exception.details['missing_fields'])

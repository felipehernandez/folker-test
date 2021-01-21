import pytest
from pytest import raises

from folker.model.error.load import InvalidSchemaDefinitionException
from folker.module.protobuf.action import ProtobufStageAction, ProtobufMethod


class TestProtobufAction:
    action: ProtobufStageAction

    @pytest.fixture(autouse=True)
    def setup(self):
        self.action = ProtobufStageAction()
        yield

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

        with raises(InvalidSchemaDefinitionException) as execution_context:
            self.action.validate()

        assert 'action.method' in execution_context.value.details['missing_fields']

    def test_validate_missing_attribute_package(self):
        self.action.method = ProtobufMethod.CREATE
        self.action.clazz = 'AClass'
        self.action.data = {'attribute_1': 'value_1'}

        with raises(InvalidSchemaDefinitionException) as execution_context:
            self.action.validate()

        assert 'action.package' in execution_context.value.details['missing_fields']

    def test_validate_missing_attribute_class(self):
        self.action.method = ProtobufMethod.CREATE
        self.action.package = 'a_protobuf_package'
        self.action.data = {'attribute_1': 'value_1'}

        with raises(InvalidSchemaDefinitionException) as execution_context:
            self.action.validate()

        assert 'action.class' in execution_context.value.details['missing_fields']

    def test_validate_missing_attribute_data(self):
        self.action.method = ProtobufMethod.CREATE
        self.action.package = 'a_protobuf_package'
        self.action.clazz = 'AClass'

        with raises(InvalidSchemaDefinitionException) as execution_context:
            self.action.validate()

        assert 'action.data' in execution_context.value.details['missing_fields']

    def test_validate_missing_attribute_message(self):
        self.action.method = ProtobufMethod.LOAD
        self.action.package = 'a_protobuf_package'
        self.action.clazz = 'AClass'

        with raises(InvalidSchemaDefinitionException) as execution_context:
            self.action.validate()

        assert 'action.message' in execution_context.value.details['missing_fields']

import sys
from unittest.mock import Mock, patch

import pytest
from pytest import raises

from folker.model.context import Context
from folker.model.error.load import InvalidSchemaDefinitionException
from folker.module.grpc.action import GrpcAction


class TestGrpcAction:
    action: GrpcAction

    @pytest.fixture(autouse=True)
    def setup(self):
        self.action = GrpcAction()
        yield

    def test_validate_correct(self):
        self.action.host = 'a_host'
        self.action.package = 'a_package'
        self.action.stub = 'a_stub'
        self.action.method = 'a_method'

        self.action.validate()

    def test_validate_full_correct(self):
        self.action.host = 'a_host'
        self.action.uri = 'a_uri'
        self.action.package = 'a_package'
        self.action.stub = 'a_stub'
        self.action.method = 'a_method'
        self.action.data = 'a_data'

        self.action.validate()

    def test_validate_missing_attribute_host(self):
        self.action.package = 'a_package'
        self.action.stub = 'a_stub'
        self.action.method = 'a_method'

        with raises(InvalidSchemaDefinitionException) as execution_context:
            self.action.validate()

        assert 'action.host' in execution_context.value.details['missing_fields']

    def test_validate_missing_attribute_package(self):
        self.action.host = 'a_host'
        self.action.stub = 'a_stub'
        self.action.method = 'a_method'

        with raises(InvalidSchemaDefinitionException) as execution_context:
            self.action.validate()

        assert 'action.package' in execution_context.value.details['missing_fields']

    def test_validate_missing_attribute_stub(self):
        self.action.host = 'a_host'
        self.action.package = 'a_package'
        self.action.method = 'a_method'

        with raises(InvalidSchemaDefinitionException) as execution_context:
            self.action.validate()

        assert 'action.stub' in execution_context.value.details['missing_fields']

    def test_validate_missing_attribute_method(self):
        self.action.host = 'a_host'
        self.action.package = 'a_package'
        self.action.stub = 'a_stub'

        with raises(InvalidSchemaDefinitionException) as execution_context:
            self.action.validate()

        assert 'action.method' in execution_context.value.details['missing_fields']

    @patch('grpc.insecure_channel')
    def test_execution_get(self, mocked_grpc):
        logger = Mock()

        self.action.host = 'a_host'
        self.action.package = 'a_package'
        self.action.stub = 'a_stub'
        self.action.method = 'a_method'
        self.action.data = 'data_value'

        mocked_channel = Mock()
        mocked_module = Mock()
        mocked_stub = Mock()
        mocked_method = Mock()
        mocked_grpc.return_value = mocked_channel
        sys.modules['a_package'] = mocked_module
        mocked_module.a_stub = mocked_stub
        mocked_stub.return_value.a_method = mocked_method
        mocked_response = Mock(return_value='returned_value')
        mocked_method.return_value = mocked_response

        context = self.action.execute(logger, context=Context())

        mocked_grpc.assert_called_with('a_host')
        mocked_stub.assert_called_with(mocked_channel)
        mocked_method.assert_called_with('data_value')
        assert mocked_response == context.stage_variables['response']

    @patch('grpc.insecure_channel')
    def test_execution_get_list(self, mocked_grpc):
        logger = Mock()

        self.action.host = 'a_host'
        self.action.package = 'a_package'
        self.action.stub = 'a_stub'
        self.action.method = 'a_method'
        self.action.data = 'data_value'

        mocked_channel = Mock()
        mocked_module = Mock()
        mocked_stub = Mock()
        mocked_method = Mock()
        mocked_grpc.return_value = mocked_channel
        sys.modules['a_package'] = mocked_module
        mocked_module.a_stub = mocked_stub
        mocked_stub.return_value.a_method = mocked_method
        mocked_response = Mock()
        mocked_response.__iter__ = Mock(return_value=iter(['item1', 'item2']))
        mocked_method.return_value = mocked_response

        context = self.action.execute(logger, context=Context())

        mocked_grpc.assert_called_with('a_host')
        mocked_stub.assert_called_with(mocked_channel)
        mocked_method.assert_called_with('data_value')
        assert ['item1', 'item2'] == context.stage_variables['response']

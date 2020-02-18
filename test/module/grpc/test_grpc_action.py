import sys
from unittest import TestCase
from unittest.mock import Mock, patch

from folker.model.error.load import InvalidSchemaDefinitionException
from folker.module.grpc.action import GrpcAction


class TestGrpcAction(TestCase):
    action: GrpcAction

    def setUp(self) -> None:
        self.action = GrpcAction()

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

        with self.assertRaises(InvalidSchemaDefinitionException) as execution_context:
            self.action.validate()

        self.assertTrue('action.host' in execution_context.exception.details['missing_fields'])

    def test_validate_missing_attribute_package(self):
        self.action.host = 'a_host'
        self.action.stub = 'a_stub'
        self.action.method = 'a_method'

        with self.assertRaises(InvalidSchemaDefinitionException) as execution_context:
            self.action.validate()

        self.assertTrue('action.package' in execution_context.exception.details['missing_fields'])

    def test_validate_missing_attribute_stub(self):
        self.action.host = 'a_host'
        self.action.package = 'a_package'
        self.action.method = 'a_method'

        with self.assertRaises(InvalidSchemaDefinitionException) as execution_context:
            self.action.validate()

        self.assertTrue('action.stub' in execution_context.exception.details['missing_fields'])

    def test_validate_missing_attribute_method(self):
        self.action.host = 'a_host'
        self.action.package = 'a_package'
        self.action.stub = 'a_stub'

        with self.assertRaises(InvalidSchemaDefinitionException) as execution_context:
            self.action.validate()

        self.assertTrue('action.method' in execution_context.exception.details['missing_fields'])

    @patch('grpc.insecure_channel')
    def test_execution_get(self, mocked_grpc):
        logger = Mock()

        self.action.host = 'a_host'
        self.action.package = 'a_package'
        self.action.stub = 'a_stub'
        self.action.method = 'a_method'
        self.action.data = 'date_key'

        mocked_channel = Mock()
        mocked_module = Mock()
        mocked_stub = Mock()
        mocked_method = Mock()
        mocked_grpc.return_value = mocked_channel
        sys.modules['a_package'] = mocked_module
        mocked_module.a_stub = mocked_stub
        mocked_stub.return_value.a_method = mocked_method
        mocked_method.return_value = 'returned_value'

        test_context, stage_context = self.action.execute(logger, {'date_key': 'data_value'}, {})

        mocked_grpc.assert_called_with('a_host')
        mocked_stub.assert_called_with(mocked_channel)
        mocked_method.assert_called_with('data_value')
        self.assertEqual('returned_value', stage_context['response'])
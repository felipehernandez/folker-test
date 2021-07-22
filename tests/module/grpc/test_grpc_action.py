import sys
from unittest.mock import Mock, patch

from folker.model.context import Context
from folker.module.grpc.action import GrpcStageAction


class TestGrpcAction:
    @patch('grpc.insecure_channel')
    def test_execution_get(self, mocked_grpc):
        logger = Mock()

        action = GrpcStageAction(host='a_host',
                                 package='a_package',
                                 stub='a_stub',
                                 method='a_method',
                                 data='data_value')

        mocked_channel = Mock()
        mocked_module = Mock()
        mocked_stub = Mock()
        mocked_method = Mock()
        mocked_grpc.return_value = mocked_channel
        sys.modules['a_package_pb2_grpc'] = mocked_module
        mocked_module.a_stub = mocked_stub
        mocked_stub.return_value.a_method = mocked_method
        mocked_response = Mock(return_value='returned_value')
        mocked_method.return_value = mocked_response

        context = action.execute(logger, context=Context())

        mocked_grpc.assert_called_with('a_host')
        mocked_stub.assert_called_with(mocked_channel)
        mocked_method.assert_called_with('data_value')
        assert mocked_response == context.stage_variables['response']

    @patch('grpc.insecure_channel')
    def test_execution_get_list(self, mocked_grpc):
        logger = Mock()

        action = GrpcStageAction(host='a_host',
                                 package='a_package',
                                 stub='a_stub',
                                 method='a_method',
                                 data='data_value')

        mocked_channel = Mock()
        mocked_module = Mock()
        mocked_stub = Mock()
        mocked_method = Mock()
        mocked_grpc.return_value = mocked_channel
        sys.modules['a_package_pb2_grpc'] = mocked_module
        mocked_module.a_stub = mocked_stub
        mocked_stub.return_value.a_method = mocked_method
        mocked_response = Mock()
        mocked_response.__iter__ = Mock(return_value=iter(['item1', 'item2']))
        mocked_method.return_value = mocked_response

        context = action.execute(logger, context=Context())

        mocked_grpc.assert_called_with('a_host')
        mocked_stub.assert_called_with(mocked_channel)
        mocked_method.assert_called_with('data_value')
        assert ['item1', 'item2'] == context.stage_variables['response']

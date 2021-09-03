from unittest.mock import patch, Mock

import pytest
import requests

from folker.model.context import Context
from folker.module.rest.action import RestStageAction, RestMethod


@pytest.mark.action_rest
class TestRestAction:
    action: RestStageAction

    @pytest.fixture(autouse=True)
    def setup(self):
        self.action = RestStageAction()
        yield

    @patch.object(requests, 'get')
    def test_execution_get(self, requests_get, plain_console_test_logger_on_trace):
        self.action.method = RestMethod.GET
        self.action.host = 'http://localhost:8080'

        mocked_response = Mock()
        requests_get.return_value = mocked_response
        mocked_response.status_code = 200
        mocked_response.headers = {}
        mocked_response.text = 'response_text'
        mocked_response.json.return_value = 'response_json'

        context = self.action.execute(logger=(plain_console_test_logger_on_trace),
                                      context=Context())

        assert {} == context.test_variables
        assert 200 == context.stage_variables['status_code']
        assert {} == context.stage_variables['headers']
        assert mocked_response == context.stage_variables['response']
        assert 'response_text' == context.stage_variables['response_text']
        assert 'response_json' == context.stage_variables['response_json']

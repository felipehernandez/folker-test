from unittest.mock import patch, Mock

import pytest
import requests
from pytest import raises

from folker.model.context import Context
from folker.model.error.load import InvalidSchemaDefinitionException
from folker.module.rest.action import RestStageAction, RestMethod


class TestRestAction:
    action: RestStageAction

    @pytest.fixture(autouse=True)
    def setup(self):
        self.action = RestStageAction()
        yield

    def test_validate_correct(self):
        self.action.method = RestMethod.GET
        self.action.host = 'http://localhost:8080'

        self.action.validate()

    def test_validate_missing_attribute_method(self):
        self.action.host = 'http://localhost:8080'

        with raises(InvalidSchemaDefinitionException) as execution_context:
            self.action.validate()

        assert 'action.method' in execution_context.value.details['missing_fields']

    def test_validate_missing_attribute_host(self):
        self.action.method = RestMethod.GET

        with raises(InvalidSchemaDefinitionException) as execution_context:
            self.action.validate()

        assert 'action.host' in execution_context.value.details['missing_fields']

    @patch.object(requests, 'get')
    def test_execution_get(self, requests_get):
        logger = Mock()

        self.action.method = RestMethod.GET
        self.action.host = 'http://localhost:8080'

        mocked_response = Mock()
        requests_get.return_value = mocked_response
        mocked_response.status_code = 200
        mocked_response.headers = {}
        mocked_response.text = 'response_text'
        mocked_response.json.return_value = 'response_json'

        context = self.action.execute(logger, context=Context())

        assert {} == context.test_variables
        assert 200 == context.stage_variables['status_code']
        assert {} == context.stage_variables['headers']
        assert mocked_response == context.stage_variables['response']
        assert 'response_text' == context.stage_variables['response_text']
        assert 'response_json' == context.stage_variables['response_json']

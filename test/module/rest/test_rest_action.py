from unittest import TestCase
from unittest.mock import patch, Mock

import requests

from folker.model.error.load import InvalidSchemaDefinitionException
from folker.module.rest.action import RestAction, RestMethod


class TestRestAction(TestCase):
    action: RestAction

    def setUp(self) -> None:
        self.action = RestAction()

    def test_validate_correct(self):
        self.action.method = RestMethod.GET
        self.action.host = 'http://localhost:8080'

        self.action.validate()

    def test_validate_missing_attribute_method(self):
        self.action.host = 'http://localhost:8080'

        with self.assertRaises(InvalidSchemaDefinitionException) as execution_context:
            self.action.validate()

        self.assertTrue('action.method' in execution_context.exception.details['missing_fields'])

    def test_validate_missing_attribute_host(self):
        self.action.method = RestMethod.GET

        with self.assertRaises(InvalidSchemaDefinitionException) as execution_context:
            self.action.validate()

        self.assertTrue('action.host' in execution_context.exception.details['missing_fields'])

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

        test_context, stage_context = self.action.execute(logger, test_context={}, stage_context={})

        self.assertEqual({}, test_context)
        self.assertEqual(200, stage_context['status_code'])
        self.assertEqual({}, stage_context['headers'])
        self.assertEqual(mocked_response, stage_context['response'])
        self.assertEqual('response_text', stage_context['response_text'])
        self.assertEqual('response_json', stage_context['response_json'])

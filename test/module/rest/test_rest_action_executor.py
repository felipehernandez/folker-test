from unittest import TestCase
from unittest.mock import patch, Mock

import requests

from folker.module.rest.action_executor import RestActionExecutor
from folker.module.rest.data import RestStageData


class TestRestActionExecutor(TestCase):

    @patch.object(requests, 'get')
    @patch('folker.module.rest.action_executor.replace_variables')
    def test_simple_get_execution(self, replace_variables, requests_get):
        executor = RestActionExecutor()
        executor.set_logger(Mock())

        stage_data = RestStageData(id='1',
                                   name='rest_stage',
                                   type='REST',
                                   action={
                                       'method': 'GET',
                                       'host': 'http://localhost:8080'
                                   })
        replace_variables.return_value = 'http://localhost:8080'
        mocked_response = Mock()
        requests_get.return_value = mocked_response
        mocked_response.status_code = 200
        mocked_response.headers = {}
        mocked_response.text = 'response_text'
        mocked_response.json.return_value = 'response_json'

        test_context, stage_context = executor.execute(stage_data, {}, {})

        self.assertEqual({}, test_context)
        self.assertTrue('elapsed_time' in stage_context)
        self.assertEqual(200, stage_context['status_code'])
        self.assertEqual({}, stage_context['headers'])
        self.assertEqual(mocked_response, stage_context['response'])
        self.assertEqual('response_text', stage_context['response_text'])
        self.assertEqual('response_json', stage_context['response_json'])

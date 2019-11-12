import json
import time

import requests

from folker.model.task import ActionExecutor
from folker.module.rest.data import RestStageData, RestActionData
from folker.util.variable import replace_variables, recursive_replace_variables


class RestActionExecutor(ActionExecutor):

    def execute(self, stage_data: RestStageData, test_context: dict, stage_context: dict) -> (dict, dict):
        start = time.time()

        rest_action = stage_data.action

        try:
            call_parameters = self._build_request_parameters(rest_action, stage_context, test_context)
            self._log_debug(method=rest_action.method.name, **call_parameters)

            response = {
                'GET': requests.get,
                'POST': requests.post,
                'PUT': requests.put,
                'DELETE': requests.delete,
                'PATCH': requests.patch
            }[rest_action.method.name](**call_parameters)

            stage_context['status_code'] = response.status_code
            stage_context['headers'] = response.headers
            stage_context['response'] = response
            stage_context['response_text'] = response.text
            try:
                stage_context['response_json'] = response.json()
            except:
                pass

        except Exception as e:
            self.logger.action_error(str(e))
            stage_context['error'] = e

        end = time.time()
        stage_context['elapsed_time'] = int((end - start) * 1000)

        return test_context, stage_context

    def _build_request_parameters(self, rest_action, stage_context, test_context):
        call_parameters = {'url': self._build_url(rest_action, test_context, stage_context),
                           'headers': recursive_replace_variables(test_context, stage_context, rest_action.headers)}

        if rest_action.body:
            call_parameters['data'] = rest_action.body
        elif rest_action.body_json:
            call_parameters['json'] = recursive_replace_variables(test_context, stage_context, rest_action.body_json)

        return call_parameters

    def _build_url(self, rest_action: RestActionData, test_context: dict, stage_context: dict):
        url = rest_action.host
        if rest_action.uri:
            url = url + '/' + rest_action.uri
        return replace_variables(test_context=test_context,
                                 stage_context=stage_context,
                                 text=url)

    def _log_debug(self, **parameters):
        self.logger.action_debug(json.dumps(parameters))

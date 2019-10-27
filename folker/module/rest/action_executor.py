import time

import requests

from folker import logger
from folker.model.task import ActionExecutor
from folker.module.rest.data import RestStageData, RestActionData
from folker.util.variable import replace_variables, recursive_replace_variables


class RestActionExecutor(ActionExecutor):

    def execute(self, stage_data: RestStageData, test_context: dict, stage_context: dict) -> (dict, dict):
        start = time.time()

        rest_action = stage_data.action

        try:
            response = {
                'GET': self._do_get,
                'POST': self._do_post,
                'PUT': self._do_put
            }[rest_action.method.name](rest_action, test_context, stage_context)

            stage_context['status_code'] = response.status_code
            stage_context['headers'] = response.headers
            stage_context['response'] = response
            stage_context['response_text'] = response.text
            try:
                stage_context['response_json'] = response.json()
            except:
                pass

        except Exception as e:
            stage_context['error'] = e

        end = time.time()
        stage_context['elapsed_time'] = int((end - start) * 1000)

        return test_context, stage_context

    def _build_url(self, rest_action: RestActionData, test_context: dict, stage_context: dict):
        url = rest_action.host
        if rest_action.uri:
            url = url + '/' + rest_action.uri
        return replace_variables(test_context=test_context,
                                 stage_context=stage_context,
                                 text=url)

    def _do_get(self, rest_action: RestActionData, test_context: dict, stage_context: dict):
        url = self._build_url(rest_action, test_context, stage_context)

        headers = rest_action.headers

        self._log_debug(method=rest_action.method.name,
                        url=url,
                        headers=headers,
                        json=None)
        logger.action_debug('url:{url}\nheaders{headers}'.format(url=url,
                                                                 headers=headers))
        return requests.get(url=url, headers=headers)

    def _do_post(self, rest_action: RestActionData, test_context: dict, stage_context: dict):
        url = self._build_url(rest_action, test_context, stage_context)
        headers = rest_action.headers

        resolved_json = recursive_replace_variables(test_context, stage_context, rest_action.body_json)

        self._log_debug(method=rest_action.method.name,
                        url=url,
                        headers=headers,
                        json=resolved_json)
        return requests.post(url=url, headers=headers, json=resolved_json)

    def _do_put(self, rest_action: RestActionData, test_context: dict, stage_context: dict):
        url = self._build_url(rest_action, test_context, stage_context)
        headers = rest_action.headers

        resolved_json = recursive_replace_variables(test_context, stage_context, rest_action.body_json)

        self._log_debug(method=rest_action.method.name,
                        url=url,
                        headers=headers,
                        json=resolved_json)
        return requests.put(url=url, headers=headers, json=resolved_json)

    def _log_debug(self, method: str, url: str, headers: dict, json=None):
        logger.action_debug('[{method}]\turl:{url}\n\theaders:{headers}\n\tbody:{body}'.format(method=method,
                                                                                               url=url,
                                                                                               headers=headers,
                                                                                               body=json))

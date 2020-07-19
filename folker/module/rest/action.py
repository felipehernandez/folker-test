import json
import time
from copy import deepcopy
from enum import Enum, auto

import requests

from folker.logger.logger import TestLogger
from folker.model.entity import Action
from folker.model.error.load import InvalidSchemaDefinitionException
from folker.util.variable import replace_variables, recursive_replace_variables


class RestMethod(Enum):
    GET = auto()
    POST = auto()
    PUT = auto()
    DELETE = auto()
    PATCH = auto()


class RestAction(Action):
    method: RestMethod
    host: str
    uri: str
    params = dict()
    headers = dict()
    body = str
    body_json = str
    data = dict()

    def __init__(self,
                 method: str = None,
                 host: str = None,
                 uri: str = None,
                 params: dict = {},
                 headers: dict = {},
                 body=None,
                 data=None,
                 json=None,
                 **kargs) -> None:
        super().__init__()

        if method:
            try:
                self.method = RestMethod[method]
            except:
                raise InvalidSchemaDefinitionException(wrong_fields=['action.method'])

        self.host = host
        self.uri = uri
        self.query_parameters = params if params else {}
        self.headers = headers if headers else {}
        self.body = body
        self.body_json = json
        self.data = data
        self.params = params

    def __copy__(self):
        return deepcopy(self)

    def enrich(self, template: 'RestAction'):
        self._set_attribute_if_missing(template, 'method')
        self._set_attribute_if_missing(template, 'host')
        self._set_attribute_if_missing(template, 'uri')
        self._set_attribute_if_missing(template, 'query_parameters')
        self._set_attribute_if_missing(template, 'headers')
        self._set_attribute_if_missing(template, 'body')
        self._set_attribute_if_missing(template, 'json')
        self._set_attribute_if_missing(template, 'data')

    def validate(self):
        missing_fields = []

        if not hasattr(self, 'method') or not self.method:
            missing_fields.append('action.method')
        if not hasattr(self, 'host') or not self.host:
            missing_fields.append('action.host')

        if len(missing_fields) > 0:
            raise InvalidSchemaDefinitionException(missing_fields=missing_fields)

    def execute(self, logger: TestLogger, test_context: dict, stage_context: dict) -> (dict, dict):
        start = time.time()

        try:
            call_parameters = self._build_request_parameters(stage_context, test_context)
            self._log_debug(logger=logger, method=self.method.name, **call_parameters)

            response = {
                RestMethod.GET: requests.get,
                RestMethod.POST: requests.post,
                RestMethod.PUT: requests.put,
                RestMethod.DELETE: requests.delete,
                RestMethod.PATCH: requests.patch
            }[self.method](**call_parameters)

            stage_context['status_code'] = response.status_code
            stage_context['headers'] = response.headers
            stage_context['response'] = response
            stage_context['response_text'] = response.text
            try:
                self._log_debug(logger=logger,
                                status_code=response.status_code,
                                response=response.text)
                stage_context['response_json'] = response.json()
            except:
                pass

        except Exception as e:
            logger.action_error(str(e))
            stage_context['error'] = e

        end = time.time()
        stage_context['elapsed_time'] = int((end - start) * 1000)

        return test_context, stage_context

    def _build_request_parameters(self, stage_context, test_context):
        call_parameters = {'url': self._build_url(test_context, stage_context),
                           'headers': recursive_replace_variables(test_context, stage_context, self.headers)}

        if self.body:
            call_parameters['data'] = recursive_replace_variables(test_context, stage_context, self.body)
        elif self.data:
            call_parameters['data'] = recursive_replace_variables(test_context, stage_context, self.data)
        elif self.body_json:
            call_parameters['headers']['Content-Type'] = 'application/json'
            call_parameters['json'] = recursive_replace_variables(test_context, stage_context, self.body_json)

        if self.params:
            call_parameters['params'] = self.params

        return call_parameters

    def _build_url(self, test_context: dict, stage_context: dict):
        url = self.host
        if self.uri:
            url = url + '/' + self.uri
        return replace_variables(test_context=test_context,
                                 stage_context=stage_context,
                                 text=url)

    def _log_debug(self, logger: TestLogger, **parameters):
        logger.action_debug(json.dumps(parameters))

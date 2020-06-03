import json
from enum import Enum, auto

import requests

from folker.logger.logger import TestLogger
from folker.model.entity import Action
from folker.model.error.load import InvalidSchemaDefinitionException
from folker.util.decorator import timed_action, resolvable_variables, loggable


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

    def mandatory_fields(self) -> [str]:
        return [
            'method',
            'host'
        ]

    @loggable
    @resolvable_variables
    @timed_action
    def execute(self, logger: TestLogger, test_context: dict, stage_context: dict) -> (dict, dict):
        try:
            call_parameters = self._build_request_parameters()
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

        return test_context, stage_context

    def _build_request_parameters(self):
        call_parameters = {'url': self._build_url(), 'headers': self.headers}

        if self.body:
            call_parameters['data'] = self.body
        elif self.data:
            call_parameters['data'] = self.data
        elif self.body_json:
            call_parameters['headers']['Content-Type'] = 'application/json'
            call_parameters['json'] = self.body_json

        if self.params:
            call_parameters['params'] = self.params

        return call_parameters

    def _build_url(self):
        return (self.host + '/' + self.uri) if self.uri else self.host

    def _log_debug(self, logger: TestLogger, **parameters):
        logger.action_debug(json.dumps(parameters))

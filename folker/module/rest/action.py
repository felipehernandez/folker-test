import json
from enum import Enum, auto
from typing import List

import requests
from mergedeep import merge

from folker.decorator import timed_action, resolvable_variables, loggable_action
from folker.logger import TestLogger
from folker.model import Context
from folker.model import StageAction
from folker.model.error import InvalidSchemaDefinitionException
from folker.module.void.action import VoidStageAction


class RestMethod(Enum):
    GET = auto()
    POST = auto()
    PUT = auto()
    DELETE = auto()
    PATCH = auto()


class RestStageAction(StageAction):
    method: RestMethod
    host: str
    uri: str
    params = dict()
    headers = dict()
    authorization: dict = dict()
    body = str
    body_json = str
    data = dict()

    def __init__(
        self,
        method: str = None,
        host: str = None,
        uri: str = None,
        params: dict = None,
        headers: dict = None,
        authorization: dict = None,
        body=None,
        data=None,
        json=None,
        **kargs
    ) -> None:
        super().__init__()

        if method:
            try:
                self.method = RestMethod[method]
            except Exception as ex:
                raise InvalidSchemaDefinitionException(wrong_fields=["action.method"])

        self.host = host
        self.uri = uri
        self.params = params if params else {}
        self.headers = headers if headers else {}
        self.authorization = authorization if authorization else {}
        self.body = body
        self.body_json = json
        self.data = data

    def __add__(self, enrichment: "RestStageAction"):
        result = self.__copy__()
        if isinstance(enrichment, VoidStageAction):
            return result

        if enrichment.host:
            result.host = enrichment.host
        if enrichment.uri:
            result.uri = enrichment.uri
        result.params = {**self.params, **enrichment.params}
        result.headers = {**self.headers, **enrichment.headers}
        result.authorization = {**self.authorization, **enrichment.authorization}
        if enrichment.body:
            result.body = enrichment.body
        if enrichment.data:
            result.data = enrichment.data
        if enrichment.body_json or enrichment.body_json:
            self_json = self.body_json if self.body_json else {}
            template_json = enrichment.body_json if enrichment.body_json else {}
            result.body_json = merge(self_json, template_json)

        return result

    def mandatory_fields(self) -> List[str]:
        return ["method", "host"]

    @loggable_action
    @resolvable_variables
    @timed_action
    def execute(self, logger: TestLogger, context: Context) -> Context:
        try:
            call_parameters = self.build_request_parameters()
            self._log_debug(logger=logger, method=self.method.name, **call_parameters)

            response = {
                RestMethod.GET: requests.get,
                RestMethod.POST: requests.post,
                RestMethod.PUT: requests.put,
                RestMethod.DELETE: requests.delete,
                RestMethod.PATCH: requests.patch,
            }[self.method](**call_parameters)

            context.save_on_stage("status_code", response.status_code)
            context.save_on_stage("headers", response.headers)
            context.save_on_stage("response", response)
            context.save_on_stage("response_text", response.text)
            try:
                self._log_debug(
                    logger=logger,
                    status_code=response.status_code,
                    response=response.text,
                )
                context.save_on_stage("response_json", response.json())
            except Exception as ex:
                pass

        except Exception as e:
            logger.action_error(str(e))
            context.save_on_stage("error", e)

        return context

    def build_request_parameters(self) -> dict:
        call_parameters = {"url": self._build_url(), "headers": self.headers}

        if self.authorization:
            call_parameters["auth"] = (
                self.authorization["user"],
                self.authorization["password"],
            )

        if self._is_form_data():
            call_parameters["headers"].pop("Content-Type")
            call_parameters["files"] = self.data

        elif self.body_json:
            call_parameters["headers"]["Content-Type"] = "application/json"
            call_parameters["json"] = self.body_json

        elif self.body:
            call_parameters["data"] = self.body

        elif self.data:
            call_parameters["data"] = self.data

        call_parameters["params"] = self.params

        return call_parameters

    def _is_form_data(self):
        return (
            "Content-Type" in self.headers
            and self.headers["Content-Type"] == "multipart/form-data"
        )

    def _build_url(self):
        return (self.host + "/" + self.uri) if self.uri else self.host

    def _log_debug(self, logger: TestLogger, **parameters):
        logger.action_debug(json.dumps(parameters))

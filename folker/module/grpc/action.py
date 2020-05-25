from collections import Iterable
from copy import deepcopy

import grpc

from folker.logger.logger import TestLogger
from folker.model.entity import Action
from folker.model.error.load import InvalidSchemaDefinitionException
from folker.util.decorator import timed_action, resolvable_variables
from folker.util.variable import resolve_variable_reference


class GrpcAction(Action):
    host: str
    uri: str

    package: str
    stub: str
    method: str
    data: object

    def __init__(self,
                 host: str = None,
                 uri: str = None,
                 package: str = None,
                 stub: str = None,
                 method: str = None,
                 data: str = None,
                 **kargs) -> None:
        super().__init__()

        self.host = host
        self.uri = uri

        self.package = package + '_pb2_grpc' if package else None
        self.stub = stub
        self.method = method

        self.data = data

    def __copy__(self):
        return deepcopy(self)

    def enrich(self, template: 'GrpcAction'):
        self._set_attribute_if_missing(template, 'host')
        self._set_attribute_if_missing(template, 'uri')
        self._set_attribute_if_missing(template, 'package')
        self._set_attribute_if_missing(template, 'stub')
        self._set_attribute_if_missing(template, 'method')
        self._set_attribute_if_missing(template, 'data')

    def validate(self):
        missing_fields = []

        if not hasattr(self, 'host') or not self.host:
            missing_fields.append('action.host')
        if not hasattr(self, 'package') or not self.package:
            missing_fields.append('action.package')
        if not hasattr(self, 'stub') or not self.stub:
            missing_fields.append('action.stub')
        if not hasattr(self, 'method') or not self.method:
            missing_fields.append('action.method')

        if len(missing_fields) > 0:
            raise InvalidSchemaDefinitionException(missing_fields=missing_fields)

    @resolvable_variables
    @timed_action
    def execute(self, logger: TestLogger, test_context: dict, stage_context: dict) -> (dict, dict):
        url = self._build_url(stage_context)
        channel = grpc.insecure_channel(url)

        imported_module = __import__(self.package, fromlist=[self.stub])
        StubDefinition = getattr(imported_module, self.stub)
        stub = StubDefinition(channel)

        method_to_call = getattr(stub, self.method)
        response = method_to_call(self.data)

        if isinstance(response, Iterable):
            stage_context['response'] = []
            for item in response:
                stage_context['response'].append(item)
        else:
            stage_context['response'] = response

        return test_context, stage_context

    def _build_url(self, stage_context: dict):
        return (self.host + '/' + self.uri) if self.uri else self.host

from collections.abc import Iterable

import grpc

from folker.decorator import timed_action, resolvable_variables, loggable_action
from folker.logger import TestLogger
from folker.model import Context
from folker.model import StageAction
from folker.module.void.action import VoidStageAction


class GrpcStageAction(StageAction):
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

        self.package = package if package else None
        self.stub = stub
        self.method = method

        self.data = data

    def __add__(self, enrichment: 'GrpcStageAction'):
        result = self.__copy__()
        if isinstance(enrichment, VoidStageAction):
            return result

        if enrichment.host:
            result.host = enrichment.host
        if enrichment.uri:
            result.uri = enrichment.uri
        if enrichment.package:
            result.package = enrichment.package
        if enrichment.stub:
            result.stub = enrichment.stub
        if enrichment.method:
            result.method = enrichment.method
        if enrichment.data:
            result.data = enrichment.data

        return result

    def mandatory_fields(self):
        return [
            'host',
            'package',
            'stub',
            'method',
        ]

    @loggable_action
    @resolvable_variables
    @timed_action
    def execute(self, logger: TestLogger, context: Context) -> Context:
        url = self._build_url()
        channel = grpc.insecure_channel(url)

        imported_module = __import__(self.package + '_pb2_grpc', fromlist=[self.stub])
        StubDefinition = getattr(imported_module, self.stub)
        stub = StubDefinition(channel)

        method_to_call = getattr(stub, self.method)
        response = method_to_call(self.data)

        if isinstance(response, Iterable):
            responses = []
            for item in response:
                responses.append(item)
            context.save_on_stage('response', responses)
        else:
            context.save_on_stage('response', response)

        return context

    def _build_url(self):
        return (self.host + '/' + self.uri) if self.uri else self.host

from collections import Iterable

import grpc

from folker.logger.logger import TestLogger
from folker.model.entity import Action
from folker.util.decorator import timed_action, resolvable_variables, loggable


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

    def mandatory_fields(self):
        return [
            'host',
            'package',
            'stub',
            'method',
        ]

    @loggable
    @resolvable_variables
    @timed_action
    def execute(self, logger: TestLogger, test_context: dict, stage_context: dict) -> (dict, dict):
        url = self._build_url()
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

    def _build_url(self):
        return (self.host + '/' + self.uri) if self.uri else self.host

from collections import Iterable

import grpc

from folker.logger import TestLogger
from folker.model import Context
from folker.model import StageAction
from folker.decorator import timed_action, resolvable_variables, loggable_action


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

    @loggable_action
    @resolvable_variables
    @timed_action
    def execute(self, logger: TestLogger, context: Context) -> Context:
        url = self._build_url()
        channel = grpc.insecure_channel(url)

        imported_module = __import__(self.package, fromlist=[self.stub])
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

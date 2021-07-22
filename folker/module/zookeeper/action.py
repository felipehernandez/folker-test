from enum import Enum, auto

from kazoo.client import KazooClient

from folker.decorator import timed_action, resolvable_variables, loggable_action
from folker.logger import TestLogger
from folker.model import Context
from folker.model import StageAction
from folker.model.error import InvalidSchemaDefinitionException
from folker.module.void.action import VoidStageAction


class ZookeeperMethod(Enum):
    EXISTS = auto()
    CREATE = auto()
    DELETE = auto()
    GET = auto()
    SET = auto()


class ZookeeperStageAction(StageAction):
    host: str
    method: ZookeeperMethod
    node = str
    data = str
    ephemeral = bool
    version: int

    def __init__(self,
                 method: str = None,
                 host: str = None,
                 node: str = None,
                 data: str = None,
                 ephemeral: bool = False,
                 version: int = -1,
                 **kargs) -> None:
        super().__init__()

        if method:
            try:
                self.method = ZookeeperMethod[method]
            except Exception as ex:
                raise InvalidSchemaDefinitionException(wrong_fields=['action.method'])

        self.host = host
        self.node = node
        self.data = data
        self.ephemeral = ephemeral
        self.version = version

    def __add__(self, enrichment: 'ZookeeperStageAction'):
        result = self.__copy__()
        if isinstance(enrichment, VoidStageAction):
            return result

        if enrichment.host:
            result.host = enrichment.host
        if enrichment.node:
            result.node = enrichment.node
        if enrichment.data:
            result.data = enrichment.data
        if enrichment.ephemeral:
            result.ephemeral = enrichment.ephemeral
        if enrichment.version:
            result.version = enrichment.version

        return result

    def mandatory_fields(self) -> [str]:
        return [
            'method',
            'host',
            'node'
        ]

    def _validate_specific(self):
        if hasattr(self, 'method') and ZookeeperMethod.SET is self.method:
            if not hasattr(self, 'data') or not self.data:
                self.validation_report.missing_fields.add('action.data')

    @loggable_action
    @resolvable_variables
    @timed_action
    def execute(self, logger: TestLogger, context: Context) -> Context:
        zookeeper = KazooClient(hosts=self.host)
        zookeeper.start()

        {
            ZookeeperMethod.EXISTS: self._exists,
            ZookeeperMethod.CREATE: self._create,
            ZookeeperMethod.DELETE: self._delete,
            ZookeeperMethod.GET: self._get,
            ZookeeperMethod.SET: self._set,
        }[self.method](logger, context, zookeeper)

        zookeeper.stop()

        return context

    def _exists(self, logger: TestLogger, context: Context, client: KazooClient):
        context.save_on_stage('path', self.node if client.exists(self.node) else None)

    def _create(self, logger: TestLogger, context: Context, client: KazooClient):
        try:
            result = client.create(path=self.node,
                                   makepath=True,
                                   value=str.encode(self.data) if self.data else b"",
                                   include_data=self.data is not None,
                                   ephemeral=self.ephemeral)
            if isinstance(result, tuple):
                context.save_on_stage('path', result[0])
                context.save_on_stage('stats', result[1])
            else:
                context.save_on_stage('path', result)
        except Exception as e:
            context.save_on_stage('error', str(e))

    def _delete(self, logger: TestLogger, context: Context, client: KazooClient):
        client.delete(self.node)

    def _get(self, logger: TestLogger, context: Context, client: KazooClient):
        data, stats = client.get(self.node)
        context.save_on_stage('data', data.decode())
        context.save_on_stage('stats', stats)

    def _set(self, logger: TestLogger, context: Context, client: KazooClient):
        stats = client.set(path=self.node,
                           value=str.encode(self.data) if self.data else b"",
                           version=self.version if self.version else -1)
        context.save_on_stage('stats', stats)

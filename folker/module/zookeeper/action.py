from enum import Enum, auto

from kazoo.client import KazooClient

from folker.decorator import timed_action, resolvable_variables, loggable_action
from folker.logger import TestLogger
from folker.model import Context
from folker.model import StageAction
from folker.model.error import InvalidSchemaDefinitionException


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
            except:
                raise InvalidSchemaDefinitionException(wrong_fields=['action.method'])

        self.host = host
        self.node = node
        self.data = data
        self.ephemeral = ephemeral
        self.version = version

    def mandatory_fields(self) -> [str]:
        return [
            'method',
            'host',
            'node'
        ]

    def validate_specific(self, missing_fields):
        if hasattr(self, 'method') and ZookeeperMethod.SET is self.method:
            missing_fields.extend(self._validate_put_values())

        return missing_fields

    def _validate_create_values(self) -> [str]:
        missing_fields = []

        if not hasattr(self, 'data'):
            missing_fields.append('action.data')

        return missing_fields

    def _validate_put_values(self) -> [str]:
        missing_fields = []

        if not hasattr(self, 'data'):
            missing_fields.append('action.data')

        return missing_fields

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

from contextlib import contextmanager
from enum import Enum, auto
from typing import Iterator, List

from kazoo.client import KazooClient

from folker.decorator import timed_action, resolvable_variables, loggable_action
from folker.logger import TestLogger
from folker.model import Context
from folker.model import StageAction
from folker.model.error import InvalidSchemaDefinitionException
from folker.module.timeout import effective_timeout
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
    ephemeral: bool = None
    version: int = None
    timeout: float = None

    def __init__(
        self,
        method: str = None,
        host: str = None,
        node: str = None,
        data: str = None,
        ephemeral: bool = None,
        version: int = None,
        timeout: float = None,
        **kargs
    ) -> None:
        super().__init__()

        if method:
            try:
                self.method = ZookeeperMethod[method]
            except Exception:
                raise InvalidSchemaDefinitionException(wrong_fields=["action.method"])

        self.host = host
        self.node = node
        self.data = data
        self.ephemeral = ephemeral
        self.version = version
        self.timeout = timeout

    def __add__(self, enrichment: "ZookeeperStageAction"):
        result = self.__copy__()
        if isinstance(enrichment, VoidStageAction):
            return result
        self._merge_method(result, enrichment)

        if enrichment.host:
            result.host = enrichment.host
        if enrichment.node:
            result.node = enrichment.node
        if enrichment.data:
            result.data = enrichment.data
        if enrichment.ephemeral is not None:
            result.ephemeral = enrichment.ephemeral
        if enrichment.version is not None:
            result.version = enrichment.version
        if enrichment.timeout is not None:
            result.timeout = enrichment.timeout

        return result

    def _connect(self) -> KazooClient:
        zookeeper = KazooClient(hosts=self.host)
        try:
            zookeeper.start(timeout=effective_timeout(self.timeout))
        except BaseException:
            # A failed start leaves the client's connection thread running
            self._disconnect(zookeeper)
            raise
        return zookeeper

    @contextmanager
    def _session(self) -> Iterator[KazooClient]:
        # BUG-23: disconnect even when the operation raises, or the session and its connection
        # thread (and the session's ephemeral nodes) stay alive until the process ends
        zookeeper = self._connect()
        try:
            yield zookeeper
        finally:
            self._disconnect(zookeeper)

    @staticmethod
    def _disconnect(zookeeper: KazooClient) -> None:
        # kazoo: close() frees the client's resources and must follow stop()
        try:
            zookeeper.stop()
        finally:
            zookeeper.close()

    def mandatory_fields(self) -> List[str]:
        return ["method", "host", "node"]

    def _validate_specific(self):
        pass

    @loggable_action
    @resolvable_variables
    @timed_action
    def execute(self, logger: TestLogger, context: Context) -> Context:
        pass


class ZookeeperStageExistsAction(ZookeeperStageAction):
    def __init__(self, **fields):
        super().__init__(**fields)

    def _validate_specific(self):
        pass

    @loggable_action
    @resolvable_variables
    @timed_action
    def execute(self, logger: TestLogger, context: Context) -> Context:
        with self._session() as zookeeper:
            context.save_on_stage(
                "path", self.node if zookeeper.exists(self.node) else None
            )

        return context


class ZookeeperStageCreateAction(ZookeeperStageAction):
    def __init__(self, **fields):
        super().__init__(**fields)

    def _validate_specific(self):
        pass

    @loggable_action
    @resolvable_variables
    @timed_action
    def execute(self, logger: TestLogger, context: Context) -> Context:
        with self._session() as zookeeper:
            self._create(logger, context, zookeeper)

        return context

    def _create(self, logger: TestLogger, context: Context, client: KazooClient):
        try:
            result = client.create(
                path=self.node,
                makepath=True,
                value=str.encode(self.data) if self.data else b"",
                include_data=self.data is not None,
                ephemeral=bool(self.ephemeral),
            )
            if isinstance(result, tuple):
                context.save_on_stage("path", result[0])
                context.save_on_stage("stats", result[1])
            else:
                context.save_on_stage("path", result)
        except Exception as e:
            context.save_on_stage("error", str(e))


class ZookeeperStageDeleteAction(ZookeeperStageAction):
    def __init__(self, **fields):
        super().__init__(**fields)

    def _validate_specific(self):
        pass

    @loggable_action
    @resolvable_variables
    @timed_action
    def execute(self, logger: TestLogger, context: Context) -> Context:
        with self._session() as zookeeper:
            zookeeper.delete(self.node)

        return context


class ZookeeperStageGetAction(ZookeeperStageAction):
    def __init__(self, **fields):
        super().__init__(**fields)

    def _validate_specific(self):
        pass

    @loggable_action
    @resolvable_variables
    @timed_action
    def execute(self, logger: TestLogger, context: Context) -> Context:
        with self._session() as zookeeper:
            data, stats = zookeeper.get(self.node)
        context.save_on_stage("data", data.decode())
        context.save_on_stage("stats", stats)

        return context


class ZookeeperStageSetAction(ZookeeperStageAction):
    def __init__(self, **fields):
        super().__init__(**fields)

    def _validate_specific(self):
        if not hasattr(self, "data") or not self.data:
            self.validation_report.missing_fields.add("action.data")

    @loggable_action
    @resolvable_variables
    @timed_action
    def execute(self, logger: TestLogger, context: Context) -> Context:
        with self._session() as zookeeper:
            stats = zookeeper.set(
                path=self.node,
                value=str.encode(self.data) if self.data else b"",
                version=self.version if self.version is not None else -1,
            )
        context.save_on_stage("stats", stats)

        return context

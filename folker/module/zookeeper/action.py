from enum import Enum, auto
from typing import List

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

    def __init__(
        self,
        method: str = None,
        host: str = None,
        node: str = None,
        data: str = None,
        ephemeral: bool = False,
        version: int = -1,
        **kargs
    ) -> None:
        super().__init__()

        if method:
            try:
                self.method = ZookeeperMethod[method]
            except Exception as ex:
                raise InvalidSchemaDefinitionException(wrong_fields=["action.method"])

        self.host = host
        self.node = node
        self.data = data
        self.ephemeral = ephemeral
        self.version = version

    def __add__(self, enrichment: "ZookeeperStageAction"):
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
        zookeeper = KazooClient(hosts=self.host)
        zookeeper.start()

        context.save_on_stage(
            "path", self.node if zookeeper.exists(self.node) else None
        )

        zookeeper.stop()

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
        zookeeper = KazooClient(hosts=self.host)
        zookeeper.start()

        self._create(logger, context, zookeeper)

        zookeeper.stop()

        return context

    def _create(self, logger: TestLogger, context: Context, client: KazooClient):
        try:
            result = client.create(
                path=self.node,
                makepath=True,
                value=str.encode(self.data) if self.data else b"",
                include_data=self.data is not None,
                ephemeral=self.ephemeral,
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
        zookeeper = KazooClient(hosts=self.host)
        zookeeper.start()

        zookeeper.delete(self.node)

        zookeeper.stop()

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
        zookeeper = KazooClient(hosts=self.host)
        zookeeper.start()

        data, stats = zookeeper.get(self.node)
        context.save_on_stage("data", data.decode())
        context.save_on_stage("stats", stats)

        zookeeper.stop()

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
        zookeeper = KazooClient(hosts=self.host)
        zookeeper.start()

        stats = zookeeper.set(
            path=self.node,
            value=str.encode(self.data) if self.data else b"",
            version=self.version if self.version else -1,
        )
        context.save_on_stage("stats", stats)

        zookeeper.stop()

        return context

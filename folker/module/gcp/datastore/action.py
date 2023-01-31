import json
import os
from copy import deepcopy
from enum import Enum, auto
from typing import List

from google.cloud.datastore import Client, Entity

from folker.decorator import loggable_action, resolvable_variables, timed_action
from folker.logger import TestLogger
from folker.model import Context, StageAction
from folker.module.void.action import VoidStageAction


class DatastoreMethod(Enum):
    PUT = auto()
    GET = auto()
    DELETE = auto()
    QUERY = auto()
    BULK_DELETE = auto()


class DatastoreStageAction(StageAction):
    method: DatastoreMethod = None

    host: str
    project: str
    credentials_path: str

    key: dict
    entity: dict

    def __init__(
        self,
        method: str = None,
        host: str = None,
        project: str = None,
        credentials: str = None,
        key: dict = None,
        entity: dict = None,
        **kargs,
    ) -> None:
        super().__init__()

        if method:
            try:
                self.method = DatastoreMethod[method]
            except Exception as ex:
                self.validation_report.wrong_fields.add("action.method")

        self.host = host
        self.project = project
        self.credentials_path = credentials

        self.key = key if key else {}
        self.entity = entity

    def __copy__(self):
        return deepcopy(self)

    def __add__(self, enrichment: "DatastoreStageAction"):
        result = self.__copy__()
        if isinstance(enrichment, VoidStageAction):
            return result

        if enrichment.host:
            result.host = enrichment.host
        if enrichment.project:
            result.project = enrichment.project
        if enrichment.credentials_path:
            result.credentials_path = enrichment.credentials_path
        if enrichment.entity:
            result.entity = enrichment.entity
        if enrichment.key:
            result.key = enrichment.key

        return result

    def mandatory_fields(self) -> List[str]:
        return ["project", "method", "key"]

    def _validate_specific(self):
        pass

    @loggable_action
    @resolvable_variables
    @timed_action
    def execute(self, logger: TestLogger, context: Context) -> Context:
        pass

    def _authenticate(self, logger: TestLogger):
        credentials_path = os.getcwd() + "credentials/gcp/gcp-credentials.json"
        credentials_path.replace("//", "/")
        if os.path.exists(credentials_path):
            logger.action_debug(f"Credentials found at {credentials_path}")
            self.credentials_path = credentials_path
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.credentials_path
        else:
            logger.action_warn(f"No credentials found at {credentials_path}")

        if self.host:
            os.environ["DATASTORE_EMULATOR_HOST"] = self.host

    def _key(self, datastore_client):
        id_or_name = self.key.get("id") if self.key.get("id") else self.key.get("name")
        return datastore_client.key(self.key.get("kind"), id_or_name)

    @staticmethod
    def _log_debug(logger: TestLogger, **parameters):
        logger.action_debug(json.dumps(parameters))


class DatastoreStagePutAction(DatastoreStageAction):
    method: DatastoreMethod = None

    host: str
    project: str
    credentials_path: str

    key: dict
    entity: dict

    def __init__(self, **fields):
        super().__init__(**fields)

    def _validate_specific(self):
        if self.key.get("kind") is None:
            self.validation_report.missing_fields.add("action.key.kind")
        if self.key.get("id") is None and self.key.get("name") is None:
            self.validation_report.missing_fields.update(
                {"action.key.id", "action.key.name"}
            )
        if not hasattr(self, "entity") or not self.entity:
            self.validation_report.missing_fields.add("action.entity")

    @loggable_action
    @resolvable_variables
    @timed_action
    def execute(self, logger: TestLogger, context: Context) -> Context:
        self._authenticate(logger)

        datastore_client = Client(project=self.project)

        key = self._key(datastore_client)
        entity = Entity(key=key)
        entity.update(self.entity)

        datastore_client.put(entity)

        return context


class DatastoreStageGetAction(DatastoreStageAction):
    method: DatastoreMethod = None

    host: str
    project: str
    credentials_path: str

    key: dict
    entity: dict

    def __init__(self, **fields):
        super().__init__(**fields)

    def _validate_specific(self):
        if self.key.get("kind") is None:
            self.validation_report.missing_fields.add("action.key.kind")
        if self.key.get("id") is None and self.key.get("name") is None:
            self.validation_report.missing_fields.update(
                {"action.key.id", "action.key.name"}
            )

    @loggable_action
    @resolvable_variables
    @timed_action
    def execute(self, logger: TestLogger, context: Context) -> Context:
        self._authenticate(logger)

        datastore_client = Client(project=self.project)

        key = self._key(datastore_client)
        entity = datastore_client.get(key)

        if entity:
            context.save_on_stage("key", dict())
            context.save_on_stage("key.kind", entity.key.kind)
            context.save_on_stage("key.id", entity.key.id)
            context.save_on_stage("key.name", entity.key.name)
            context.save_on_stage("entity", entity.copy())
        else:
            context.save_on_stage("key", None)
            context.save_on_stage("entity", None)

        return context


class DatastoreStageDeleteAction(DatastoreStageAction):
    method: DatastoreMethod = None

    host: str
    project: str
    credentials_path: str

    key: dict
    entity: dict

    def __init__(self, **fields):
        super().__init__(**fields)

    def _validate_specific(self):
        if self.key.get("kind") is None:
            self.validation_report.missing_fields.add("action.key.kind")
        if self.key.get("id") is None and self.key.get("name") is None:
            self.validation_report.missing_fields.update(
                {"action.key.id", "action.key.name"}
            )

    @loggable_action
    @resolvable_variables
    @timed_action
    def execute(self, logger: TestLogger, context: Context) -> Context:
        self._authenticate(logger)

        datastore_client = Client(project=self.project)

        key = self._key(datastore_client)
        datastore_client.delete(key)

        return context


class DatastoreStageBulkDeleteAction(DatastoreStageAction):
    method: DatastoreMethod = None

    host: str
    project: str
    credentials_path: str

    key: dict
    entity: dict

    def __init__(self, **fields):
        super().__init__(**fields)

    def _validate_specific(self):
        if self.key.get("kind") is None:
            self.validation_report.missing_fields.add("action.key.kind")

    @loggable_action
    @resolvable_variables
    @timed_action
    def execute(self, logger: TestLogger, context: Context) -> Context:
        self._authenticate(logger)

        datastore_client = Client(project=self.project)

        id_or_names = (
            self.key.get("ids") if self.key.get("ids") else self.key.get("names")
        )
        keyss = [
            datastore_client.key(self.key.get("kind"), id_or_name)
            for id_or_name in id_or_names
        ]
        total_keys_size = len(keyss)

        for keys in self._divide_chunks(keyss, 500):
            datastore_client.delete_multi(keys)
            logger.action_debug(f"Bulk deleted {len(keys)} items of {total_keys_size}")

        return context

    def _divide_chunks(self, l, chunk_size):
        for i in range(0, len(l), chunk_size):
            yield l[i : i + chunk_size]


class DatastoreStageQueryAction(DatastoreStageAction):
    method: DatastoreMethod = None

    host: str
    project: str
    credentials_path: str

    key: dict
    entity: dict

    def __init__(self, **fields):
        super().__init__(**fields)

    def _validate_specific(self):
        if self.key.get("kind") is None:
            self.validation_report.missing_fields.add("action.key.kind")

    @loggable_action
    @resolvable_variables
    @timed_action
    def execute(self, logger: TestLogger, context: Context) -> Context:
        self._authenticate(logger)

        datastore_client = Client(project=self.project)

        query = datastore_client.query(kind=self.key.get("kind"))
        result = [entity for entity in query.fetch()]

        context.save_on_stage("result", result)

        return context

import json
import os
from copy import deepcopy
from enum import Enum, auto

from google.cloud import datastore

from folker.logger.logger import TestLogger
from folker.model.context import Context
from folker.model.error.load import InvalidSchemaDefinitionException
from folker.model.stage.action import Action
from folker.util.decorator import timed_action, resolvable_variables, loggable


class DatastoreMethod(Enum):
    PUT = auto()
    GET = auto()
    DELETE = auto()
    QUERY = auto()
    BULK_DELETE = auto()


def _divide_chunks(l, chunk_size):
    for i in range(0, len(l), chunk_size):
        yield l[i:i + chunk_size]


class DatastoreAction(Action):
    method: DatastoreMethod

    host: str
    project: str
    credentials_path: str

    key: dict
    entity: dict

    def __init__(self,
                 method: str = None,
                 host: str = None,
                 project: str = None,
                 credentials: str = None,
                 key: dict = None,
                 entity: dict = None,
                 **kargs) -> None:
        super().__init__()

        if method:
            try:
                self.method = DatastoreMethod[method]
            except:
                raise InvalidSchemaDefinitionException(wrong_fields=['action.method'])

        self.host = host
        self.project = project
        self.credentials_path = credentials

        self.key = key
        self.entity = entity

    def __copy__(self):
        return deepcopy(self)

    def mandatory_fields(self):
        return [
            'project',
            'method',
            'key'
        ]

    def validate_specific(self, missing_fields):
        if self.key.get('kind') is None:
            missing_fields.append('action.key.kind')
        if self.method in [DatastoreMethod.PUT, DatastoreMethod.GET, DatastoreMethod.DELETE] and \
                self.key.get('id') is None and self.key.get('name') is None:
            missing_fields.append('action.key.id')
            missing_fields.append('action.key.name')
        if hasattr(self, 'method') and DatastoreMethod.PUT is self.method:
            missing_fields.extend(self._validate_put_values())

        return missing_fields

    def _validate_put_values(self):
        missing_fields = []

        if not hasattr(self, 'entity') or not self.entity:
            missing_fields.append('action.entity')

        return missing_fields

    @loggable
    @resolvable_variables
    @timed_action
    def execute(self, logger: TestLogger, context: Context) -> Context:
        self._authenticate(logger)

        datastore_client = datastore.Client(project=self.project)

        {
            DatastoreMethod.PUT: self._put,
            DatastoreMethod.GET: self._get,
            DatastoreMethod.DELETE: self._delete,
            DatastoreMethod.QUERY: self._query,
            DatastoreMethod.BULK_DELETE: self._bulk_delete,
        }.get(self.method)(logger, context, datastore_client)

        return context

    def _authenticate(self, logger: TestLogger):
        credentials_path = os.getcwd() + 'credentials/gcp/gcp-credentials.json'
        credentials_path.replace('//', '/')
        if os.path.exists(credentials_path):
            logger.action_debug('Credentials found at {}'.format(credentials_path))
            self.credentials_path = credentials_path
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.credentials_path
        else:
            logger.action_warn('No credentials found at {}'.format(credentials_path))

        if self.host:
            os.environ["DATASTORE_EMULATOR_HOST"] = self.host

    def _key(self, datastore_client):
        id_or_name = self.key.get('id') if self.key.get('id') else self.key.get('name')
        return datastore_client.key(self.key.get('kind'), id_or_name)

    def _put(self, logger: TestLogger, context: Context, datastore_client):
        key = self._key(datastore_client)
        entity = datastore.Entity(key=key)
        entity.update(self.entity)

        datastore_client.put(entity)

    def _get(self, logger: TestLogger, context: Context, datastore_client):
        key = self._key(datastore_client)
        entity = datastore_client.get(key)

        if entity:
            context.save_on_stage('key', dict())
            context.save_on_stage('key.kind', entity.key.kind)
            context.save_on_stage('key.id', entity.key.id)
            context.save_on_stage('key.name', entity.key.name)
            context.save_on_stage('entity', entity.copy())
        else:
            context.save_on_stage('key', None)
            context.save_on_stage('entity', None)

    def _delete(self, logger: TestLogger, context: Context, datastore_client):
        key = self._key(datastore_client)
        datastore_client.delete(key)

    def _bulk_delete(self, logger: TestLogger, context: Context, datastore_client):
        id_or_names = self.key.get('ids') if self.key.get('ids') else self.key.get('names')
        keyss = [datastore_client.key(self.key.get('kind'), id_or_name) for id_or_name in id_or_names]
        total_keys_size = len(keyss)

        for keys in _divide_chunks(keyss, 500):
            datastore_client.delete_multi(keys)
            logger.action_debug('Bulk deleted {} items of {}'.format(len(keys), total_keys_size))

    def _query(self, logger: TestLogger, context: Context, datastore_client):
        query = datastore_client.query(kind=self.key.get('kind'))
        result = [entity for entity in query.fetch()]

        context.save_on_stage('result', result)

    @staticmethod
    def _log_debug(logger: TestLogger, **parameters):
        logger.action_debug(json.dumps(parameters))

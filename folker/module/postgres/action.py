import time
from copy import deepcopy
from enum import Enum, auto

import psycopg2

from folker.logger.logger import TestLogger
from folker.model.entity import Action
from folker.model.error.load import InvalidSchemaDefinitionException
from folker.util.variable import replace_variables


class PostgresMethod(Enum):
    CREATE = auto()
    DELETE = auto()
    DROP = auto()
    INSERT = auto()
    SELECT = auto()
    UPDATE = auto()


IS_FETCH = {
    PostgresMethod.CREATE: False,
    PostgresMethod.INSERT: False,
    PostgresMethod.SELECT: True,
}


class PostgresAction(Action):
    method: PostgresMethod
    host: str
    port: str
    user: str
    password: str
    database: str
    sql: str

    def __init__(self,
                 method: str = None,
                 host: str = None,
                 port: str = None,
                 user: str = None,
                 password: str = None,
                 database: str = None,
                 sql: str = None,
                 **kargs) -> None:
        super().__init__()
        if method:
            try:
                self.method = PostgresMethod[method]
            except:
                raise InvalidSchemaDefinitionException(wrong_fields=['action.method'])

        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.sql = sql

    def __copy__(self):
        return deepcopy(self)

    def enrich(self, template: 'PostgresAction'):
        self._set_attribute_if_missing(template, 'method')
        self._set_attribute_if_missing(template, 'host')
        self._set_attribute_if_missing(template, 'port')
        self._set_attribute_if_missing(template, 'user')
        self._set_attribute_if_missing(template, 'password')
        self._set_attribute_if_missing(template, 'database')
        self._set_attribute_if_missing(template, 'sql')

    def validate(self):
        missing_fields = []

        if not hasattr(self, 'method') or not self.method:
            missing_fields.append('action.method')
        if not hasattr(self, 'host') or not self.host:
            missing_fields.append('action.host')
        if not hasattr(self, 'port') or not self.port:
            self.host = '5432'
        if not hasattr(self, 'user') or not self.user:
            missing_fields.append('action.user')
        if not hasattr(self, 'password') or not self.password:
            missing_fields.append('action.password')
        if not hasattr(self, 'database') or not self.database:
            missing_fields.append('action.database')
        if not hasattr(self, 'sql') or not self.sql:
            missing_fields.append('action.sql')

        if len(missing_fields) > 0:
            raise InvalidSchemaDefinitionException(missing_fields=missing_fields)

    def execute(self, logger: TestLogger, test_context: dict, stage_context: dict) -> (dict, dict):
        start = time.time()

        user = replace_variables(test_context=test_context, stage_context=stage_context, text=self.user)
        password = replace_variables(test_context=test_context, stage_context=stage_context, text=self.password)
        host = replace_variables(test_context=test_context, stage_context=stage_context, text=self.host)
        port = replace_variables(test_context=test_context, stage_context=stage_context, text=self.port)
        database = replace_variables(test_context=test_context, stage_context=stage_context, text=self.database)

        try:
            connection = psycopg2.connect(user=user,
                                          password=password,
                                          host=host,
                                          port=port,
                                          database=database)
            logger.action_debug('Connected to {}:{}/{} as {}'.format(self.host, self.port, self.database, self.user))

            cursor = connection.cursor()
            cursor.execute(self.sql)
            if IS_FETCH.get(self.method, False):
                records = cursor.fetchall()
                columns = cursor.description
                result = [
                    {
                        columns[i].name: record[i]
                        for i in range(len(record))
                    }
                    for record in records
                ]
                stage_context['result'] = result
            else:
                connection.commit()
        except (Exception, psycopg2.Error) as error:
            logger.action_error(str(error))
            stage_context['error'] = error
        finally:
            # closing database connection.
            if (connection):
                cursor.close()
                connection.close()
                logger.action_debug('Disconnected from {}:{}/{} as {}'.format(self.host, self.port, self.database, self.user))

        end = time.time()
        stage_context['elapsed_time'] = int((end - start) * 1000)

        return test_context, stage_context

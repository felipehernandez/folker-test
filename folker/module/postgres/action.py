from enum import Enum, auto

import psycopg2

from folker.logger.logger import TestLogger
from folker.model.stage.action import Action
from folker.model.error.load import InvalidSchemaDefinitionException
from folker.util.decorator import timed_action, resolvable_variables, loggable


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

    def mandatory_fields(self):
        return [
            'method',
            'host',
            'port',
            'user',
            'password',
            'database',
            'sql'
        ]

    @loggable
    @resolvable_variables
    @timed_action
    def execute(self, logger: TestLogger, test_context: dict, stage_context: dict) -> (dict, dict):
        try:
            connection = psycopg2.connect(user=self.user,
                                          password=self.password,
                                          host=self.host,
                                          port=self.port,
                                          database=self.database)
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

        return test_context, stage_context

from enum import Enum, auto

import psycopg2

from folker.decorator import timed_action, resolvable_variables, loggable_action
from folker.logger import TestLogger
from folker.model import Context
from folker.model import StageAction
from folker.module.void.action import VoidStageAction


class PostgresMethod(Enum):
    CREATE = auto()
    DELETE = auto()
    DROP = auto()
    INSERT = auto()
    SELECT = auto()
    UPDATE = auto()


class PostgresStageAction(StageAction):
    method: PostgresMethod
    host: str
    port: str
    user: str
    password: str
    database: str
    sql: str

    def __init__(
        self,
        method: str = None,
        host: str = None,
        port: str = None,
        user: str = None,
        password: str = None,
        database: str = None,
        sql: str = None,
        **kargs,
    ) -> None:
        super().__init__()
        if method:
            try:
                self.method = PostgresMethod[method]
            except Exception as ex:
                self.validation_report.wrong_fields.add("action.method")

        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.sql = sql

    def __add__(self, enrichment: "PostgresStageAction"):
        result = self.__copy__()
        if isinstance(enrichment, VoidStageAction):
            return result

        if enrichment.host:
            result.host = enrichment.host
        if enrichment.port:
            result.port = enrichment.port
        if enrichment.user:
            result.user = enrichment.user
        if enrichment.password:
            result.password = enrichment.password
        if enrichment.database:
            result.database = enrichment.database
        if enrichment.sql:
            result.sql = enrichment.sql

        return result

    def mandatory_fields(self):
        return ["method", "host", "port", "user", "password", "database", "sql"]

    @loggable_action
    @resolvable_variables
    @timed_action
    def execute(self, logger: TestLogger, context: Context) -> Context:
        try:
            connection = psycopg2.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                database=self.database,
            )
            logger.action_debug(
                f"Connected to {self.host}:{self.port}/{self.database} as {self.user}"
            )

            cursor = connection.cursor()
            cursor.execute(self.sql)
            if self._has_data_to_fetch():
                records = cursor.fetchall()
                columns = cursor.description
                result = [
                    {columns[i].name: record[i] for i in range(len(record))}
                    for record in records
                ]
                context.save_on_stage("result", result)
            else:
                connection.commit()
        except (Exception, psycopg2.Error) as error:
            logger.action_error(str(error))
            context.save_on_stage("error", error)
        finally:
            # closing database connection.
            if connection:
                cursor.close()
                connection.close()
                logger.action_debug(
                    f"Disconnected from {self.host}:{self.port}/{self.database} as {self.user}"
                )

        return context

    def _has_data_to_fetch(self):
        return False


class PostgresStageCreateAction(PostgresStageAction):
    def __init__(self, **fields):
        super().__init__(**fields)

    def _has_data_to_fetch(self):
        return False


class PostgresStageDeleteAction(PostgresStageAction):
    def __init__(self, **fields):
        super().__init__(**fields)

    def _has_data_to_fetch(self):
        return False


class PostgresStageDropAction(PostgresStageAction):
    def __init__(self, **fields):
        super().__init__(**fields)

    def _has_data_to_fetch(self):
        return False


class PostgresStageInsertAction(PostgresStageAction):
    def __init__(self, **fields):
        super().__init__(**fields)

    def _has_data_to_fetch(self):
        return False


class PostgresStageSelectAction(PostgresStageAction):
    def __init__(self, **fields):
        super().__init__(**fields)

    def _has_data_to_fetch(self):
        return False


class PostgresStageUpdateAction(PostgresStageAction):
    def __init__(self, **fields):
        super().__init__(**fields)

    def _has_data_to_fetch(self):
        return False

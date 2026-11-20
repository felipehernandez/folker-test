from types import SimpleNamespace
from unittest.mock import patch

import psycopg2
import pytest

from folker.logger import TestLogger
from folker.model import Context
from folker.module.postgres.action import (PostgresStageCreateAction, PostgresStageDeleteAction,
                                           PostgresStageDropAction, PostgresStageInsertAction,
                                           PostgresStageSelectAction, PostgresStageUpdateAction)

CONNECT = 'folker.module.postgres.action.psycopg2.connect'
DEFINITION = dict(host='db-host', port='5432', user='the-user', password='the-password',
                  database='the-database', sql='select 1')


def action(cls=PostgresStageSelectAction, **fields):
    return cls(**{**DEFINITION, **fields})


@pytest.fixture
def logger(mocker):
    return mocker.Mock(spec=TestLogger)


@pytest.fixture
def connection():
    with patch(CONNECT) as connect:
        connect.return_value.cursor.return_value.fetchall.return_value = []
        yield connect.return_value


@pytest.mark.action_postgres
class TestPostgresConnection:
    @patch(CONNECT)
    def test_it_connects_with_the_definition(self, connect, logger):
        connect.return_value.cursor.return_value.fetchall.return_value = []

        action().execute(logger=logger, context=Context())

        kwargs = connect.call_args.kwargs
        assert (kwargs['host'], kwargs['port'], kwargs['user'], kwargs['password'],
                kwargs['database']) == ('db-host', '5432', 'the-user', 'the-password',
                                        'the-database')

    def test_the_sql_is_executed(self, connection, logger):
        action(sql='select * from users').execute(logger=logger, context=Context())

        connection.cursor.return_value.execute.assert_called_once_with('select * from users')

    def test_variables_are_resolved_in_every_field(self, connection, logger):
        context = Context(test_variables={'table': 'users', 'host': 'resolved-host'},
                          secrets={'password': 'resolved-password'})

        with patch(CONNECT, return_value=connection) as connect:
            action(sql='select * from ${table}', host='${host}', password='${password}') \
                .execute(logger=logger, context=context)

        connection.cursor.return_value.execute.assert_called_once_with('select * from users')
        assert connect.call_args.kwargs['host'] == 'resolved-host'
        assert connect.call_args.kwargs['password'] == 'resolved-password'

    def test_the_connection_and_the_cursor_are_closed(self, connection, logger):
        action().execute(logger=logger, context=Context())

        connection.cursor.return_value.close.assert_called_once()
        connection.close.assert_called_once()

    def test_connecting_and_disconnecting_are_logged_without_the_password(self, connection, logger):
        action().execute(logger=logger, context=Context())

        messages = [call.args[0] for call in logger.action_debug.call_args_list]
        assert messages == ['Connected to db-host:5432/the-database as the-user',
                            'Disconnected from db-host:5432/the-database as the-user']
        assert 'the-password' not in ' '.join(messages)


@pytest.mark.action_postgres
class TestPostgresStatements:
    @pytest.mark.parametrize('cls', [PostgresStageCreateAction, PostgresStageDeleteAction,
                                     PostgresStageDropAction, PostgresStageInsertAction,
                                     PostgresStageUpdateAction],
                             ids=lambda cls: cls.__name__[len('PostgresStage'):-len('Action')])
    def test_statements_that_change_data_are_committed_and_save_no_result(
            self, cls, connection, logger):
        context = action(cls).execute(logger=logger, context=Context())

        connection.commit.assert_called_once()
        connection.cursor.return_value.fetchall.assert_not_called()
        assert 'result' not in context.stage_variables

    def test_a_select_returns_the_rows_as_dictionaries_and_does_not_commit(
            self, connection, logger):
        cursor = connection.cursor.return_value
        cursor.description = [SimpleNamespace(name='id'), SimpleNamespace(name='name')]
        cursor.fetchall.return_value = [(1, 'folker'), (2, 'test')]

        context = action().execute(logger=logger, context=Context())

        assert context.stage_variables['result'] == [{'id': 1, 'name': 'folker'},
                                                     {'id': 2, 'name': 'test'}]
        connection.commit.assert_not_called()

    def test_a_select_without_rows_saves_an_empty_list(self, connection, logger):
        connection.cursor.return_value.description = [SimpleNamespace(name='id')]

        context = action().execute(logger=logger, context=Context())

        assert context.stage_variables['result'] == []


@pytest.mark.action_postgres
class TestPostgresFailures:
    def test_a_failing_statement_is_reported_without_failing_the_action(self, connection, logger):
        connection.cursor.return_value.execute.side_effect = psycopg2.errors.UndefinedTable(
            'relation "nope" does not exist')

        context = action(sql='select * from nope').execute(logger=logger, context=Context())

        assert isinstance(context.stage_variables['error'], psycopg2.errors.UndefinedTable)
        logger.action_error.assert_called_once()
        assert 'nope' in logger.action_error.call_args.args[0]
        assert 'result' not in context.stage_variables

    def test_a_failing_statement_is_not_committed_and_the_connection_is_closed(
            self, connection, logger):
        connection.cursor.return_value.execute.side_effect = psycopg2.Error('failed')

        action(PostgresStageInsertAction).execute(logger=logger, context=Context())

        connection.commit.assert_not_called()
        connection.cursor.return_value.close.assert_called_once()
        connection.close.assert_called_once()

    def test_a_failure_to_connect_is_reported_without_failing_the_action(self, logger):
        with patch(CONNECT, side_effect=psycopg2.OperationalError('connection refused')):
            context = action().execute(logger=logger, context=Context())

        assert isinstance(context.stage_variables['error'], psycopg2.OperationalError)
        logger.action_error.assert_called_once_with('connection refused')

    def test_nothing_is_logged_as_disconnected_when_the_connection_never_opened(self, logger):
        with patch(CONNECT, side_effect=psycopg2.OperationalError('connection refused')):
            action().execute(logger=logger, context=Context())

        logger.action_debug.assert_not_called()

    def test_a_failure_while_reading_the_rows_is_reported_and_closes_everything(
            self, connection, logger):
        connection.cursor.return_value.fetchall.side_effect = psycopg2.Error('lost connection')

        context = action().execute(logger=logger, context=Context())

        assert isinstance(context.stage_variables['error'], psycopg2.Error)
        connection.close.assert_called_once()

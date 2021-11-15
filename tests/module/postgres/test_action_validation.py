import pytest

from folker.module.postgres.action import PostgresStageAction, PostgresMethod


@pytest.mark.action_correctness
@pytest.mark.action_postgres
class TestPostgresRestActionValidation:
    def test_validate_empty(self):
        action = PostgresStageAction()

        assert not action
        assert not action.validation_report
        assert 'action.method' in action.validation_report.missing_fields
        assert 'action.host' in action.validation_report.missing_fields
        assert 'action.port' in action.validation_report.missing_fields
        assert 'action.user' in action.validation_report.missing_fields
        assert 'action.password' in action.validation_report.missing_fields
        assert 'action.database' in action.validation_report.missing_fields
        assert 'action.sql' in action.validation_report.missing_fields

    def test_validate_wrong_method(self):
        action = PostgresStageAction(method='X',
                                     host='a_host',
                                     port='5432',
                                     user='a_user',
                                     password='a_password',
                                     database='a_database',
                                     sql='a_sql_statement'
                                     )

        assert not action
        assert not action.validation_report
        assert 'action.method' in action.validation_report.wrong_fields

    def test_correct(self):
        action = PostgresStageAction(method=PostgresMethod.SELECT.name,
                                     host='a_host',
                                     port='5432',
                                     user='a_user',
                                     password='a_password',
                                     database='a_database',
                                     sql='a_sql_statement')

        assert action
        assert action.validation_report

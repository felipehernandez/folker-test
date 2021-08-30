import pytest

from folker.module.postgres.action import PostgresStageAction, PostgresMethod
from folker.module.void.action import VoidStageAction


@pytest.mark.action_kafka
class TestRestActionEnrichment:
    def test_enrich_empty(self):
        original = PostgresStageAction(method=PostgresMethod.SELECT.name)
        enrichment = PostgresStageAction(method=PostgresMethod.SELECT.name,
                                         host='a_host',
                                         port='5432',
                                         user='a_user',
                                         password='a_password',
                                         database='a_database',
                                         sql='a_sql_statement')

        enriched = original + enrichment

        assert enriched.method == PostgresMethod.SELECT
        assert enriched.host == 'a_host'
        assert enriched.port == '5432'
        assert enriched.user == 'a_user'
        assert enriched.password == 'a_password'
        assert enriched.database == 'a_database'
        assert enriched.sql == 'a_sql_statement'

    def test_override_host(self):
        original = PostgresStageAction(method=PostgresMethod.SELECT.name,
                                       host='a_host',
                                       port='5432',
                                       user='a_user',
                                       password='a_password',
                                       database='a_database',
                                       sql='a_sql_statement')
        enrichment = PostgresStageAction(host='another_host')

        enriched = original + enrichment

        assert enriched.method == PostgresMethod.SELECT
        assert enriched.host == 'another_host'
        assert enriched.port == '5432'
        assert enriched.user == 'a_user'
        assert enriched.password == 'a_password'
        assert enriched.database == 'a_database'
        assert enriched.sql == 'a_sql_statement'

    def test_enrich_void(self):
        original = PostgresStageAction(method=PostgresMethod.SELECT.name,
                                       host='a_host',
                                       port='5432',
                                       user='a_user',
                                       password='a_password',
                                       database='a_database',
                                       sql='a_sql_statement')
        enrichment = VoidStageAction()

        enriched = original + enrichment

        assert enriched.method == PostgresMethod.SELECT
        assert enriched.host == 'a_host'
        assert enriched.port == '5432'
        assert enriched.user == 'a_user'
        assert enriched.password == 'a_password'
        assert enriched.database == 'a_database'
        assert enriched.sql == 'a_sql_statement'

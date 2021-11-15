import pytest

from folker.module.graphql.action import GraphQLStageAction
from folker.module.void.action import VoidStageAction


@pytest.mark.action_graphql
class TestGraphQLActionEnrichment:
    def test_enrich_empty_query(self):
        original = GraphQLStageAction()
        enrichment = GraphQLStageAction(host='a_host',
                                        uri='an_uri',
                                        query='a_query')

        enriched = original + enrichment

        assert enriched.host == 'a_host'
        assert enriched.uri == 'an_uri'
        assert enriched.query == 'a_query'

    def test_enrich_empty_mutation(self):
        original = GraphQLStageAction()
        enrichment = GraphQLStageAction(host='a_host',
                                        uri='an_uri',
                                        mutation='a_mutation')

        enriched = original + enrichment

        assert enriched.host == 'a_host'
        assert enriched.uri == 'an_uri'
        assert enriched.mutation == 'a_mutation'

    def test_override_query(self):
        original = GraphQLStageAction(host='a_host',
                                      uri='an_uri',
                                      query='a_query')
        enrichment = GraphQLStageAction(query='another_query')

        enriched = original + enrichment

        assert enriched.host == 'a_host'
        assert enriched.uri == 'an_uri'
        assert enriched.query == 'another_query'

    def test_override_mutation(self):
        original = GraphQLStageAction(host='a_host',
                                      uri='an_uri',
                                      mutation='a_mutation')
        enrichment = GraphQLStageAction(mutation='another_mutation')

        enriched = original + enrichment

        assert enriched.host == 'a_host'
        assert enriched.uri == 'an_uri'
        assert enriched.mutation == 'another_mutation'

    def test_enrich_void(self):
        original = GraphQLStageAction(host='a_host',
                                      uri='an_uri',
                                      query='a_query')
        enrichment = VoidStageAction()

        enriched = original + enrichment

        assert enriched.host == 'a_host'
        assert enriched.uri == 'an_uri'
        assert enriched.query == 'a_query'

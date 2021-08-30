import pytest

from folker.module.gcp.pubsub.action import PubSubStageAction, PubSubMethod
from folker.module.void.action import VoidStageAction


@pytest.mark.action_gcp_pubsub
class TestPubSubActionEnrichment:
    def test_enrich_override(self):
        original = PubSubStageAction(method=PubSubMethod.PUBLISH.name,
                                     project='a-project',
                                     topic='a-topic',
                                     attributes={'an-attribute': 'a_value'})
        enrichment = PubSubStageAction(message='message')

        enriched = original + enrichment

        assert enriched.method == PubSubMethod.PUBLISH
        assert enriched.project == 'a-project'
        assert enriched.topic == 'a-topic'
        assert enriched.attributes == {'an-attribute': 'a_value'}
        assert enriched.message == 'message'

    def test_enrich_merge_attributes(self):
        original = PubSubStageAction(method=PubSubMethod.PUBLISH.name,
                                     project='a-project',
                                     topic='a-topic',
                                     message='message',
                                     attributes={'an-attribute': 'a_value'})
        enrichment = PubSubStageAction(attributes={'another-attribute': 'another_value'})

        enriched = original + enrichment

        assert enriched.method == PubSubMethod.PUBLISH
        assert enriched.project == 'a-project'
        assert enriched.topic == 'a-topic'
        assert enriched.attributes == {'an-attribute': 'a_value',
                                       'another-attribute': 'another_value'}
        assert enriched.message == 'message'

    def test_enrich_void(self):
        original = PubSubStageAction(method=PubSubMethod.PUBLISH.name,
                                     project='a-project',
                                     topic='a-topic',
                                     attributes={'an-attribute': 'value'},
                                     message='message')
        enrichment = VoidStageAction()

        enriched = original + enrichment

        assert enriched.method == PubSubMethod.PUBLISH
        assert enriched.project == 'a-project'
        assert enriched.topic == 'a-topic'
        assert enriched.attributes == {'an-attribute': 'value'}
        assert enriched.message == 'message'

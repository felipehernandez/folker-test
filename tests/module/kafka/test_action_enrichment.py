from folker.module.kafka.action import KafkaStageAction, KafkaMethod
from folker.module.void.action import VoidStageAction


class TestKafkaActionEnrichment:
    def test_enrich_merge_headers(self):
        original = KafkaStageAction(method=KafkaMethod.PUBLISH.name,
                                    host='a_host',
                                    topic='a_topic',
                                    key='a_key',
                                    headers={'key1': 'value1'})
        enrichment = KafkaStageAction(method=KafkaMethod.PUBLISH.name,
                                      headers={'key2': 'value2'})

        enriched = original + enrichment

        assert enriched.method == KafkaMethod.PUBLISH
        assert enriched.host == 'a_host'
        assert enriched.topic == 'a_topic'
        assert enriched.key == 'a_key'
        assert enriched.headers == {'key1': 'value1', 'key2': 'value2'}

    def test_enrich_void(self):
        original = KafkaStageAction(method=KafkaMethod.PUBLISH.name,
                                    host='a_host',
                                    topic='a_topic',
                                    key='a_key')
        enrichment = VoidStageAction()

        enriched = original + enrichment

        assert enriched.method == KafkaMethod.PUBLISH
        assert enriched.host == 'a_host'
        assert enriched.topic == 'a_topic'
        assert enriched.key == 'a_key'

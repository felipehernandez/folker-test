import pytest

from folker.module.rabbitmq.action import RabbitMQStageAction, RabbitMQMethod
from folker.module.void.action import VoidStageAction


@pytest.mark.action_rabbitmq
class TestRabbitMQActionEnrichment:
    def test_enrich_message(self):
        original = RabbitMQStageAction(method=RabbitMQMethod.PUBLISH.name,
                                       host='a_host',
                                       exchange='an_exchange',
                                       message='Old message')
        enrichment = RabbitMQStageAction(method=RabbitMQMethod.PUBLISH.name,
                                         message='New message')

        enriched = original + enrichment

        assert enriched.method == RabbitMQMethod.PUBLISH
        assert enriched.host == 'a_host'
        assert enriched.exchange == 'an_exchange'
        assert enriched.message == 'New message'

    def test_enrich_ack(self):
        original = RabbitMQStageAction(method=RabbitMQMethod.SUBSCRIBE.name,
                                       host='a_host',
                                       queue='a_queue',
                                       ack=False)
        enrichment = RabbitMQStageAction(method=RabbitMQMethod.SUBSCRIBE.name,
                                         ack=True)

        enriched = original + enrichment

        assert enriched.method == RabbitMQMethod.SUBSCRIBE
        assert enriched.host == 'a_host'
        assert enriched.queue == 'a_queue'
        assert enriched.ack == True

    def test_enrich_void(self):
        original = RabbitMQStageAction(method=RabbitMQMethod.PUBLISH.name,
                                       host='a_host',
                                       exchange='an_exchange',
                                       message='A message')
        enrichment = VoidStageAction()

        enriched = original + enrichment

        assert enriched.method == RabbitMQMethod.PUBLISH
        assert enriched.host == 'a_host'
        assert enriched.exchange == 'an_exchange'
        assert enriched.message == 'A message'

import pytest
from google.cloud.pubsub import PublisherClient, SubscriberClient
from google.pubsub_v1.services.publisher.transports import PublisherGrpcTransport
from google.pubsub_v1.services.subscriber.transports import SubscriberGrpcTransport

from folker.module.gcp.pubsub.action import _publisher_client, _subscriber_client


# The other pubsub tests replace PublisherClient/SubscriberClient with mocks, so they accept any
# constructor arguments. google-cloud-pubsub 2.x dropped `channel=`; the integration job caught
# it (`PublisherClient.__init__() got an unexpected keyword argument 'channel'`), these tests
# build the real clients so the unit tests catch it too.
@pytest.mark.action_gcp_pubsub
class TestPubSubClients:
    @pytest.mark.parametrize('factory, client, transport', [
        (_publisher_client, PublisherClient, PublisherGrpcTransport),
        (_subscriber_client, SubscriberClient, SubscriberGrpcTransport),
    ], ids=['publisher', 'subscriber'])
    def test_a_client_for_an_emulator_host_is_built_over_a_grpc_transport(self, factory, client, transport):
        created = factory('localhost:8681')

        try:
            assert isinstance(created, client)
            assert isinstance(created.transport, transport)
        finally:
            created.transport.close()

    @pytest.mark.parametrize('factory, client', [
        (_publisher_client, PublisherClient),
        (_subscriber_client, SubscriberClient),
    ], ids=['publisher', 'subscriber'])
    def test_a_client_without_host_uses_the_default_connection(self, monkeypatch, factory, client):
        monkeypatch.setenv('PUBSUB_EMULATOR_HOST', 'localhost:8681')

        created = factory(None)

        try:
            assert isinstance(created, client)
        finally:
            created.transport.close()

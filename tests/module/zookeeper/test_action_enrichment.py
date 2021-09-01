import pytest

from folker.module.void.action import VoidStageAction
from folker.module.zookeeper.action import ZookeeperStageAction, ZookeeperMethod


@pytest.mark.action_zookeeper
class TestZookeeperActionEnrichment:
    def test_enrich_empty_exists(self):
        original = ZookeeperStageAction(ZookeeperMethod.EXISTS.name)
        enrichment = ZookeeperStageAction(method=ZookeeperMethod.EXISTS.name,
                                          host='a_host',
                                          node='a_node')

        enriched = original + enrichment

        assert enriched.method == ZookeeperMethod.EXISTS
        assert enriched.host == 'a_host'
        assert enriched.node == 'a_node'

    def test_enrich_override_exists(self):
        original = ZookeeperStageAction(ZookeeperMethod.EXISTS.name,
                                        host='a_host')
        enrichment = ZookeeperStageAction(method=ZookeeperMethod.EXISTS.name,
                                          host='another_host',
                                          node='a_node')

        enriched = original + enrichment

        assert enriched.method == ZookeeperMethod.EXISTS
        assert enriched.host == 'another_host'
        assert enriched.node == 'a_node'

    def test_enrich_void(self):
        original = ZookeeperStageAction(method=ZookeeperMethod.EXISTS.name,
                                        host='a_host',
                                        node='a_node')
        enrichment = VoidStageAction()

        enriched = original + enrichment

        assert enriched.method == ZookeeperMethod.EXISTS
        assert enriched.host == 'a_host'
        assert enriched.node == 'a_node'

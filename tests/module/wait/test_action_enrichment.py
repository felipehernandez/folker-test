from folker.module.void.action import VoidStageAction
from folker.module.wait.action import WaitStageAction


class TestWaitActionEnrichment:
    def test_enrich_empty(self):
        original = WaitStageAction()
        enrichment = WaitStageAction(time=3)

        enriched = original + enrichment

        assert enriched.time == 3

    def test_enrich_override(self):
        original = WaitStageAction(time=2)
        enrichment = WaitStageAction(time=3)

        enriched = original + enrichment

        assert enriched.time == 3

    def test_enrich_void(self):
        original = WaitStageAction(time=2)
        enrichment = VoidStageAction()

        enriched = original + enrichment

        assert enriched.time == 2
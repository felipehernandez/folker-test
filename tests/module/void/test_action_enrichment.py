import pytest

from folker.module.void.action import VoidStageAction
from folker.module.wait.action import WaitStageAction


@pytest.mark.action_void
class TestVoidActionEnrichment:
    # BUG-04: VoidStageAction.__add__ returned None, so a template stage without an action
    # (VOID) extended by a stage with an action ended up with no action at all.
    def test_enrich_with_real_action(self):
        original = VoidStageAction()
        enrichment = WaitStageAction(time=3)

        enriched = original + enrichment

        assert isinstance(enriched, WaitStageAction)
        assert enriched.time == 3

    def test_enrichment_is_a_copy(self):
        original = VoidStageAction()
        enrichment = WaitStageAction(time=3)

        enriched = original + enrichment

        assert isinstance(enriched, WaitStageAction)
        assert enriched is not enrichment

    def test_enrich_with_void(self):
        original = VoidStageAction()
        enrichment = VoidStageAction()

        enriched = original + enrichment

        assert isinstance(enriched, VoidStageAction)

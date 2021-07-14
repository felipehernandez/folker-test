from folker.module.printt.action import PrintStageAction
from folker.module.void.action import VoidStageAction


class TestPrintActionEnrichment:
    def test_enrich_empty(self):
        original = PrintStageAction()
        enrichment = PrintStageAction(message='a_message')

        enriched = original + enrichment

        assert enriched.message == 'a_message'

    def test_enrich_override(self):
        original = PrintStageAction(message='a_message')
        enrichment = PrintStageAction(message='another_message')

        enriched = original + enrichment

        assert enriched.message == 'another_message'

    def test_enrich_void(self):
        original = PrintStageAction(message='a_message')
        enrichment = VoidStageAction()

        enriched = original + enrichment

        assert enriched.message == 'a_message'

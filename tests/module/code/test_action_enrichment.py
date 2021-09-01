import pytest

from folker.module.code.action import CodeStageAction
from folker.module.void.action import VoidStageAction


@pytest.mark.action_code
class TestFileActionEnrichment:
    def test_enrich_empty(self):
        original = CodeStageAction()
        enrichment = CodeStageAction(module='a_module',
                                     method='a_method')

        enriched = original + enrichment

        assert enriched.module == 'a_module'
        assert enriched.method == 'a_method'

    def test_enrich_empty_parameters(self):
        original = CodeStageAction()
        enrichment = CodeStageAction(module='a_module',
                                     method='a_method',
                                     parameters={'a_name': 'a_value'})

        enriched = original + enrichment

        assert enriched.module == 'a_module'
        assert enriched.method == 'a_method'
        assert enriched.parameters == {'a_name': 'a_value'}

    def test_merge_parameters(self):
        original = CodeStageAction(module='a_module',
                                   method='a_method',
                                   parameters={'a_name': 'a_value'})
        enrichment = CodeStageAction(parameters={'another_name': 'another_value'})

        enriched = original + enrichment

        assert enriched.module == 'a_module'
        assert enriched.method == 'a_method'
        assert enriched.parameters == {'a_name': 'a_value', 'another_name': 'another_value'}

    def test_merge_overlapping_parameters(self):
        original = CodeStageAction(module='a_module',
                                   method='a_method',
                                   parameters={'a_name': 'a_value'})
        enrichment = CodeStageAction(parameters={'a_name': 'another_value'})

        enriched = original + enrichment

        assert enriched.module == 'a_module'
        assert enriched.method == 'a_method'
        assert enriched.parameters == {'a_name': 'another_value'}

    def test_enrich_void(self):
        original = CodeStageAction(module='a_module',
                                   method='a_method')
        enrichment = VoidStageAction()

        enriched = original + enrichment

        assert enriched.module == 'a_module'
        assert enriched.method == 'a_method'

from folker.model import Stage
from folker.module.wait.action import WaitStageAction


class TestStageEnrichment:

    def test_enrich_action(self):
        original = Stage(name='a_name',
                         action=WaitStageAction())
        enrichment = Stage(name='a_name',
                           action=WaitStageAction(time=3))

        result = original + enrichment

        assert result.action.time == 3

    def test_enrich_action_override(self):
        original = Stage(name='a_name',
                         action=WaitStageAction(time=2))
        enrichment = Stage(name='a_name',
                           action=WaitStageAction(time=3))

        result = original + enrichment

        assert result.action.time == 3

    def test_enrich_action_no_override(self):
        original = Stage(name='a_name',
                         action=WaitStageAction(time=2))
        enrichment = Stage(name='a_name',
                           action=WaitStageAction())

        result = original + enrichment

        assert result.action.time == 2

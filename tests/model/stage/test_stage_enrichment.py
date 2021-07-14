from folker.model import Stage
from folker.module.void.action import VoidStageAction
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

    def test_enrich_void_action(self):
        original = Stage(name='a_name',
                         action=WaitStageAction(time=2))
        enrichment = Stage(name='a_name',
                           action=VoidStageAction())

        result = original + enrichment

        assert result.action.time == 2

    def test_enrich_save(self):
        original = Stage(name='a_name',
                         action=WaitStageAction(time=2))
        enrichment = Stage(action=VoidStageAction(),
                           save={'a_key': 'a_value'})

        result = original + enrichment

        assert result.action.time == 2
        assert result.save.save == {'a_key': 'a_value'}

    def test_enrich_log(self):
        original = Stage(name='a_name',
                         action=WaitStageAction(time=2))
        enrichment = Stage(action=VoidStageAction(),
                           log=['a_log'])

        result = original + enrichment

        assert result.action.time == 2
        assert result.log.logs == {'a_log'}

    def test_enrich_assertions(self):
        original = Stage(name='a_name',
                         action=WaitStageAction(time=2))
        enrichment = Stage(action=VoidStageAction(),
                           assertions=['an_assertion'])

        result = original + enrichment

        assert result.action.time == 2
        assert result.assertions.assertions == {'an_assertion'}

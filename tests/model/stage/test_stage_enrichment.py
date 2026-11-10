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

    def test_enrich_action_of_void_template(self):
        # BUG-04: a template with only shared save/log/assertions, extended by a stage with an action
        original = Stage(name='a_template',
                         action=VoidStageAction(),
                         save={'a_key': 'a_value'})
        enrichment = Stage(name='a_name',
                           action=WaitStageAction(time=3))

        result = original + enrichment

        assert result.action.time == 3
        assert result.save.save == {'a_key': 'a_value'}

    # BUG-05: Stage.__add__ wrote the merged foreach to `result.params`, so it was lost
    def test_enrich_foreach(self):
        original = Stage(name='a_name',
                         action=WaitStageAction(time=2))
        enrichment = Stage(name='a_name',
                           action=VoidStageAction(),
                           foreach={'key': ['value1', 'value2']})

        result = original + enrichment

        assert result.foreach == {'key': ['value1', 'value2']}

    def test_enrich_foreach_keeps_the_template_foreach(self):
        original = Stage(name='a_name',
                         action=WaitStageAction(time=2),
                         foreach={'template_key': ['a']})
        enrichment = Stage(name='a_name',
                           action=VoidStageAction())

        result = original + enrichment

        assert result.foreach == {'template_key': ['a']}

    def test_enrich_foreach_merges_and_overrides(self):
        original = Stage(name='a_name',
                         action=WaitStageAction(time=2),
                         foreach={'shared': ['template'], 'template_key': ['a']})
        enrichment = Stage(name='a_name',
                           action=VoidStageAction(),
                           foreach={'shared': ['stage'], 'stage_key': ['b']})

        result = original + enrichment

        assert result.foreach == {'shared': ['stage'], 'template_key': ['a'], 'stage_key': ['b']}

    def test_enrich_foreach_does_not_modify_the_template(self):
        original = Stage(name='a_name',
                         action=WaitStageAction(time=2),
                         foreach={'template_key': ['a']})
        enrichment = Stage(name='a_name',
                           action=VoidStageAction(),
                           foreach={'stage_key': ['b']})

        original + enrichment

        assert original.foreach == {'template_key': ['a']}

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
        assert result.log.logs == ['a_log']

    def test_enrich_assertions(self):
        original = Stage(name='a_name',
                         action=WaitStageAction(time=2))
        enrichment = Stage(action=VoidStageAction(),
                           assertions=['an_assertion'])

        result = original + enrichment

        assert result.action.time == 2
        assert result.assertions.assertions == ['an_assertion']

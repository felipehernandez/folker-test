from unittest import TestCase

from folker.model.entity import StageSave
from folker.model.error.variables import VariableReferenceResolutionException


class TestStageSave(TestCase):
    stage: StageSave

    def setUp(self):
        self.stage = StageSave()

    def test_enrich(self):
        self.stage.save['existing'] = 'value'

        self.stage.enrich(StageSave({'new': 'Value'}))

        self.assertTrue('existing' in self.stage.save)
        self.assertEqual('value', self.stage.save.get('existing'))
        self.assertTrue('new' in self.stage.save)
        self.assertEqual('Value', self.stage.save.get('new'))

    def test_given_no_saves_then_nothing(self):
        test_context, stage_context = self.stage.execute(None, {}, {})

        self.assertEqual({}, test_context)
        self.assertEqual({}, stage_context)

    def test_given_plain_saves_then_update_test_context(self):
        self.stage.save = {'save_in': 'value_to_save'}

        test_context, stage_context = self.stage.execute(None, {}, {})

        self.assertEqual({'save_in': 'value_to_save'}, test_context)
        self.assertEqual({}, stage_context)

    def test_given_referenced_saves_then_update_test_context(self):
        self.stage.save = {'save_in': '${referenced_value_to_save}'}

        test_context, stage_context = self.stage.execute(None, {}, {'referenced_value_to_save': 'value_to_save'})

        self.assertEqual({'save_in': 'value_to_save'}, test_context)
        self.assertEqual({'referenced_value_to_save': 'value_to_save'}, stage_context)

    def test_save_variable_not_in_context(self):
        self.stage.save = {'save_in': '${referenced_value_to_save}'}

        try:
            self.stage.execute(None, {}, {})
            raise AssertionError('Should not get here')
        except VariableReferenceResolutionException as ex:
            self.assertEqual('VariableResolver', ex.source)
            self.assertEqual('Missing reference in context', ex.error)
            self.assertEqual('Variable reference cannot be resolved', ex.cause)
            self.assertTrue('referenced_value_to_save' in ex.details['reference'])

    def test_given_evaluation_string_then_update_test_context_with_evaluation(self):
        self.stage.save = {'save_in': '1 + 1'}

        test_context, stage_context = self.stage.execute(None, {}, {})

        self.assertEqual({'save_in': 2}, test_context)
        self.assertEqual({}, stage_context)

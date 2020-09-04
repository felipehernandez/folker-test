from unittest import TestCase

from folker.model.context import Context
from folker.model.error.variables import VariableReferenceResolutionException
from folker.model.stage.save import StageSave


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
        context = self.stage.execute(None, Context())

        self.assertEqual({}, context.test_variables)
        self.assertEqual({}, context.stage_variables)

    def test_given_plain_saves_then_update_test_context(self):
        self.stage.save = {'save_in': 'value_to_save'}

        context = self.stage.execute(None, Context())

        self.assertEqual({'save_in': 'value_to_save'}, context.test_variables)
        self.assertEqual({}, context.stage_variables)

    def test_given_referenced_saves_then_update_test_context(self):
        self.stage.save = {'save_in': '${referenced_value_to_save}'}

        context = self.stage.execute(None, Context({}, {'referenced_value_to_save': 'value_to_save'}))

        self.assertEqual({'save_in': 'value_to_save'}, context.test_variables)
        self.assertEqual({'referenced_value_to_save': 'value_to_save'}, context.stage_variables)

    def test_save_variable_not_in_context(self):
        self.stage.save = {'save_in': '${referenced_value_to_save}'}

        try:
            self.stage.execute(None, Context())
            raise AssertionError('Should not get here')
        except VariableReferenceResolutionException as ex:
            self.assertEqual('VariableResolver', ex.source)
            self.assertEqual('Missing reference in context', ex.error)
            self.assertEqual('Variable reference cannot be resolved', ex.cause)
            self.assertTrue('referenced_value_to_save' in ex.details['reference'])

    def test_given_evaluation_string_then_update_test_context_with_evaluation(self):
        self.stage.save = {'save_in': '1 + 1'}

        context = self.stage.execute(None, Context())

        self.assertEqual({'save_in': 2}, context.test_variables)
        self.assertEqual({}, context.stage_variables)

    def test_given_complex_save_then_complex_variable_in_context(self):
        self.stage.save = {
            'save.in.1': '0 + 1',
            'save.in.2': '1 + 1'
        }

        context = self.stage.execute(None, Context())

        self.assertEqual({'save': {'in': {'1': 1, '2': 2}}}, context.test_variables)
        self.assertEqual({}, context.stage_variables)

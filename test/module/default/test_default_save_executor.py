from unittest import TestCase

from folker.model import StageData
from folker.model.error.variables import VariableReferenceResolutionException
from folker.module.default.save_executor import DefaultSaveExecutor


class TestDefaultSaveExecutor(TestCase):

    def test_given_no_saves_then_nothing(self):
        executor = DefaultSaveExecutor()

        stage_data = StageData(
            id='default',
            name='stage_name',
            save={}
        )

        test_context, stage_context = executor.execute(stage_data, {}, {})

        self.assertEqual({}, test_context)
        self.assertEqual({}, stage_context)

    def test_given_plain_saves_then_update_test_context(self):
        executor = DefaultSaveExecutor()

        stage_data = StageData(
            id='default',
            name='stage_name',
            save={'save_in': 'value_to_save'}
        )

        test_context, stage_context = executor.execute(stage_data, {}, {})

        self.assertEqual({'save_in': 'value_to_save'}, test_context)
        self.assertEqual({}, stage_context)

    def test_given_referenced_saves_then_update_test_context(self):
        executor = DefaultSaveExecutor()

        stage_data = StageData(
            id='default',
            name='stage_name',
            save={'save_in': '${referenced_value_to_save}'}
        )

        test_context, stage_context = executor.execute(stage_data, {}, {'referenced_value_to_save': 'value_to_save'})

        self.assertEqual({'save_in': 'value_to_save'}, test_context)
        self.assertEqual({'referenced_value_to_save': 'value_to_save'}, stage_context)

    def test_given_referenced_saves_in_test_context_then_update_test_context(self):
        executor = DefaultSaveExecutor()

        stage_data = StageData(
            id='default',
            name='stage_name',
            save={'save_in': '${referenced_value_to_save}'}
        )

        try:
            executor.execute(stage_data, {'referenced_value_to_save': 'value_to_save'}, {})
        except VariableReferenceResolutionException as ex:
            self.assertEqual('VariableResolver', ex.source)
            self.assertEqual('Missing reference in context', ex.error)
            self.assertEqual('Variable reference cannot be resolved', ex.cause)
            self.assertTrue('referenced_value_to_save' in ex.details['reference'])

import pytest

from folker.model.context import Context
from folker.model.error.variables import VariableReferenceResolutionException
from folker.model.stage.save import StageSave


class TestStageSave:
    stage: StageSave

    @pytest.fixture(autouse=True)
    def setup(self):
        self.stage = StageSave()
        yield

    def test_enrich(self):
        self.stage.save['existing'] = 'value'

        self.stage.enrich(StageSave({'new': 'Value'}))

        assert 'existing' in self.stage.save
        assert 'value' == self.stage.save.get('existing')
        assert 'new' in self.stage.save
        assert 'Value' == self.stage.save.get('new')

    def test_given_no_saves_then_nothing(self):
        context = self.stage.execute(None, Context())

        assert {} == context.test_variables
        assert {} == context.stage_variables

    def test_given_plain_saves_then_update_test_context(self):
        self.stage.save = {'save_in': 'value_to_save'}

        context = self.stage.execute(None, Context())

        assert {'save_in': 'value_to_save'} == context.test_variables
        assert {} == context.stage_variables

    def test_given_referenced_saves_then_update_test_context(self):
        self.stage.save = {'save_in': '${referenced_value_to_save}'}

        context = self.stage.execute(None,
                                     Context({}, {'referenced_value_to_save': 'value_to_save'}))

        assert {'save_in': 'value_to_save'} == context.test_variables
        assert {'referenced_value_to_save': 'value_to_save'} == context.stage_variables

    def test_save_variable_not_in_context(self):
        self.stage.save = {'save_in': '${referenced_value_to_save}'}

        try:
            self.stage.execute(None, Context())
            raise AssertionError('Should not get here')
        except VariableReferenceResolutionException as ex:
            assert 'VariableResolver' == ex.source
            assert 'Missing reference in context' == ex.error
            assert 'Variable reference cannot be resolved' == ex.cause
            assert 'referenced_value_to_save' in ex.details['reference']

    def test_given_evaluation_string_then_update_test_context_with_evaluation(self):
        self.stage.save = {'save_in': '1 + 1'}

        context = self.stage.execute(None, Context())

        assert {'save_in': 2} == context.test_variables
        assert {} == context.stage_variables

    def test_given_complex_save_then_complex_variable_in_context(self):
        self.stage.save = {
            'save.in.1': '0 + 1',
            'save.in.2': '1 + 1'
        }

        context = self.stage.execute(None, Context())

        assert {'save': {'in': {'1': 1, '2': 2}}} == context.test_variables
        assert {} == context.stage_variables

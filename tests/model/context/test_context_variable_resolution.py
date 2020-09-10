from unittest import TestCase

from folker.model.context import Context
from folker.model.error.variables import VariableReferenceResolutionException


class TestContextReplication(TestCase):

    def test_given_context_when_missing_simple_variables_reference_then_Ex(self):
        context = Context(test_variables={},
                          stage_variables={},
                          secrets={})

        try:
            context.resolve_variable_reference('missing_variable')
        except VariableReferenceResolutionException as e:
            self.assertEqual('missing_variable', e.details['reference'])

    def test_given_context_when_simple_variables_reference_in_test_variables_then_value(self):
        context = Context(test_variables={'variable': 'value'},
                          stage_variables={},
                          secrets={})

        result = context.resolve_variable_reference('variable')

        self.assertEqual('value', result)

    def test_given_context_when_simple_variables_reference_in_stage_variables_then_value(self):
        context = Context(test_variables={},
                          stage_variables={'variable': 'value'},
                          secrets={})

        result = context.resolve_variable_reference('variable')

        self.assertEqual('value', result)

    def test_given_context_when_simple_variables_reference_in_secrets_then_value(self):
        context = Context(test_variables={},
                          stage_variables={'variable': 'value'},
                          secrets={})

        result = context.resolve_variable_reference('variable')

        self.assertEqual('value', result)

    def test_given_context_when_simple_variables_reference_in_all_then_stage_value(self):
        context = Context(test_variables={'variable': 'test_value'},
                          stage_variables={'variable': 'stage_value'},
                          secrets={'variable': 'secret_value'})

        result = context.resolve_variable_reference('variable')

        self.assertEqual('stage_value', result)

    def test_given_context_when_family_variables_reference_in_test_variables_then_value(self):
        context = Context(test_variables={'level0': {'level1': 'value'}},
                          stage_variables={},
                          secrets={})

        result = context.resolve_variable_reference('level0.level1')

        self.assertEqual('value', result)

    def test_given_context_when_list_variables_reference_in_test_variables_then_value(self):
        context = Context(test_variables={'level0': [{'level1': 'wrong'}, {'level1': 'value'}]},
                          stage_variables={},
                          secrets={})

        result = context.resolve_variable_reference('level0.[1].level1')

        self.assertEqual('value', result)

    def test_given_empty_context_when_plain_text_then_text(self):
        context = Context(test_variables={},
                          stage_variables={},
                          secrets={})
        result = context.replace_variables('variable')

        self.assertEqual('variable', result)

    def test_given_context_when_plain_text_then_text(self):
        context = Context(test_variables={'variable': 'value'},
                          stage_variables={},
                          secrets={})
        result = context.replace_variables('variable')

        self.assertEqual('variable', result)

    def test_given_context_when_variable_then_value(self):
        context = Context(test_variables={'variable': 'value'},
                          stage_variables={},
                          secrets={})
        result = context.replace_variables('${variable}')

        self.assertEqual('value', result)

    def test_given_context_when_complex_variable_then_value(self):
        context = Context(test_variables={'variable': {'0': 'value'}},
                          stage_variables={},
                          secrets={})
        result = context.replace_variables('${variable.0}')

        self.assertEqual('value', result)

    def test_given_context_when_list_variable_then_value(self):
        context = Context(test_variables={'variable': [{'0': 'value'}]},
                          stage_variables={},
                          secrets={})
        result = context.replace_variables('${variable.[0].0}')

        self.assertEqual('value', result)

    def test_given_context_when_text_with_variable_then_value(self):
        context = Context(test_variables={'variable': 'value'},
                          stage_variables={},
                          secrets={})
        result = context.replace_variables('-${variable}-')

        self.assertEqual('-value-', result)

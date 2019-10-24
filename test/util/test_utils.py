from unittest import TestCase

from folker.model.error.variables import VariableReferenceResolutionException
from folker.util.variable import resolve_variable_reference


class TestStringMethods(TestCase):

    def test_missing_simple_variable(self):
        try:
            result = resolve_variable_reference({}, {}, 'variable')
        except VariableReferenceResolutionException as e:
            self.assertEqual('variable', e.details['reference'])

    def test_existing_simple_variable_in_test_context(self):
        result = resolve_variable_reference({'variable': 'value'}, {}, 'variable')

        self.assertEqual('value', result)

    def test_existing_simple_variable_in_stage_context(self):
        result = resolve_variable_reference({}, {'variable': 'value'}, 'variable')

        self.assertEqual('value', result)

    def test_existing_simple_variable_in_both_contexts(self):
        result = resolve_variable_reference({'variable': 'value_test'}, {'variable': 'value_stage'}, 'variable')

        self.assertEqual('value_stage', result)

    def test_existing_family_variable_in_test_context(self):
        result = resolve_variable_reference({'level0': {'level1': 'value'}}, {}, 'level0.level1')

        self.assertEqual('value', result)

    def test_existing_list_variable_in_test_context(self):
        result = resolve_variable_reference({'level0': [{'level1': 'wrong'}, {'level1': 'value'}]}, {}, 'level0.[1].level1')

        self.assertEqual('value', result)

from unittest import TestCase

from folker.model.error.variables import VariableReferenceResolutionException
from folker.util.variable import resolve_variable_reference, extract_value_from_context, build_contexts


class TestStringMethods(TestCase):

    def test_missing_simple_variable(self):
        try:
            return resolve_variable_reference({}, {}, 'variable')
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

    def test_value_from_context_no_reference(self):
        result = extract_value_from_context({}, {}, 'variable')

        self.assertEqual('variable', result)

    def test_value_from_context_no_reference2(self):
        result = extract_value_from_context({'variable': 'value'}, {}, 'variable')

        self.assertEqual('variable', result)

    def test_value_from_context_reference(self):
        result = extract_value_from_context({'variable': 'value'}, {}, '${variable}')

        self.assertEqual('value', result)

    def test_value_from_context_complex_reference(self):
        result = extract_value_from_context({'variable': {'0': 'value'}}, {}, '${variable.0}')

        self.assertEqual('value', result)

    def test_create_empty_context(self):
        result = build_contexts({}, {}, {})

        self.assertEqual([{}], result)

    def test_create_simple_context(self):
        result = build_contexts({}, {}, {'variable1': 'value1'})

        self.assertEqual([{'variable1': 'value1', 'variable1_index': 0}], result)

    def test_create_several_contexts(self):
        result = build_contexts({}, {}, {'variable1': ['value1', 'value2']})

        self.assertEqual([{'variable1': 'value1', 'variable1_index': 0},
                          {'variable1': 'value2', 'variable1_index': 1}
                          ], result)

    def test_create_multiple_variables_several_contexts(self):
        result = build_contexts({}, {}, {'variable1': ['value11', 'value12'], 'variable2': 'value21'})

        self.assertEqual([{'variable1': 'value11', 'variable1_index': 0, 'variable2': 'value21', 'variable2_index': 0},
                          {'variable1': 'value12', 'variable1_index': 1, 'variable2': 'value21', 'variable2_index': 0}
                          ], result)

    def test_create_multiple_variables_several_contexts2(self):
        result = build_contexts({}, {}, {'variable1': ['value11', 'value12'], 'variable2': ['value21', 'value22']})

        self.assertEqual([{'variable1': 'value11', 'variable1_index': 0, 'variable2': 'value21', 'variable2_index': 0},
                          {'variable1': 'value11', 'variable1_index': 0, 'variable2': 'value22', 'variable2_index': 1},
                          {'variable1': 'value12', 'variable1_index': 1, 'variable2': 'value21', 'variable2_index': 0},
                          {'variable1': 'value12', 'variable1_index': 1, 'variable2': 'value22', 'variable2_index': 1}
                          ], result)

    def test_create_referenced_variables_several_contexts(self):
        result = build_contexts({'reference1': 'value1'}, {}, {'variable1': '${reference1}', 'variable2': ['value21', 'value22']})

        self.assertEqual([{'variable1': 'value1', 'variable1_index': 0, 'variable2': 'value21', 'variable2_index': 0},
                          {'variable1': 'value1', 'variable1_index': 0, 'variable2': 'value22', 'variable2_index': 1}
                          ], result)

    def test_create_referenced_multiple_variables_several_contexts(self):
        result = build_contexts({'reference1': ['value11', 'value12']}, {}, {'variable1': '${reference1}', 'variable2': ['value21', 'value22']})

        self.assertEqual([{'variable1': 'value11', 'variable1_index': 0, 'variable2': 'value21', 'variable2_index': 0},
                          {'variable1': 'value11', 'variable1_index': 0, 'variable2': 'value22', 'variable2_index': 1},
                          {'variable1': 'value12', 'variable1_index': 1, 'variable2': 'value21', 'variable2_index': 0},
                          {'variable1': 'value12', 'variable1_index': 1, 'variable2': 'value22', 'variable2_index': 1}
                          ], result)

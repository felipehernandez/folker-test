from unittest import TestCase

from folker.model.context import Context


class TestContextReplication(TestCase):

    def test_given_empty_context_when_no_variables_then_same_context(self):
        original_context = Context(test_variables={}, stage_variables={}, secrets={})

        generated_contexts = original_context.replicate_on_test({})

        self.assertEqual(1, len(generated_contexts))
        self.assertDictEqual(original_context.test_variables, generated_contexts[0].test_variables)
        self.assertDictEqual(original_context.stage_variables, generated_contexts[0].stage_variables)
        self.assertDictEqual(original_context.secrets, generated_contexts[0].secrets)

    def test_given_empty_context_when_replicate_test_with_one_variables_then_contexts(self):
        original_context = Context(test_variables={}, stage_variables={}, secrets={})

        generated_contexts = original_context.replicate_on_test({'variable': [1, 2]})

        self.assertEqual(2, len(generated_contexts))

        contexts_0 = generated_contexts[0]
        self.assertDictEqual({**original_context.test_variables, 'variable': 1, 'variable_index': 0},
                             contexts_0.test_variables)
        self.assertDictEqual(original_context.stage_variables, contexts_0.stage_variables)
        self.assertDictEqual(original_context.secrets, contexts_0.secrets)

        contexts_1 = generated_contexts[1]
        self.assertDictEqual({**original_context.test_variables, 'variable': 2, 'variable_index': 1},
                             contexts_1.test_variables)
        self.assertDictEqual(original_context.stage_variables, contexts_1.stage_variables)
        self.assertDictEqual(original_context.secrets, contexts_1.secrets)

    def test_given_empty_context_when_replicate_test_with_two_variables_then_contexts(self):
        original_context = Context(test_variables={}, stage_variables={}, secrets={})

        generated_contexts = original_context.replicate_on_test({'variable': [1, 2], 'variable2': ['a', 'b']})

        self.assertEqual(4, len(generated_contexts))

        generated_context = generated_contexts[0]
        self.assertDictEqual({**original_context.test_variables,
                              'variable': 1, 'variable_index': 0,
                              'variable2': 'a', 'variable2_index': 0
                              },
                             generated_context.test_variables)
        self.assertDictEqual(original_context.stage_variables, generated_context.stage_variables)
        self.assertDictEqual(original_context.secrets, generated_context.secrets)

        generated_context = generated_contexts[1]
        self.assertDictEqual({**original_context.test_variables,
                              'variable': 1, 'variable_index': 0,
                              'variable2': 'b', 'variable2_index': 1
                              },
                             generated_context.test_variables)
        self.assertDictEqual(original_context.stage_variables, generated_context.stage_variables)
        self.assertDictEqual(original_context.secrets, generated_context.secrets)

        generated_context = generated_contexts[2]
        self.assertDictEqual({**original_context.test_variables,
                              'variable': 2, 'variable_index': 1,
                              'variable2': 'a', 'variable2_index': 0
                              },
                             generated_context.test_variables)
        self.assertDictEqual(original_context.stage_variables, generated_context.stage_variables)
        self.assertDictEqual(original_context.secrets, generated_context.secrets)

        generated_context = generated_contexts[3]
        self.assertDictEqual({**original_context.test_variables,
                              'variable': 2, 'variable_index': 1,
                              'variable2': 'b', 'variable2_index': 1
                              },
                             generated_context.test_variables)
        self.assertDictEqual(original_context.stage_variables, generated_context.stage_variables)
        self.assertDictEqual(original_context.secrets, generated_context.secrets)

    def test_given_not_empty_context_when_replicate_test_with_two_variables_then_contexts(self):
        original_context = Context(test_variables={'test_vble': 'test_value'},
                                   stage_variables={'stage_vble': 'stage_value'},
                                   secrets={'secret_vble': 'secret_value'})

        generated_contexts = original_context.replicate_on_test({'variable': [1, 2], 'variable2': ['a', 'b']})

        self.assertEqual(4, len(generated_contexts))

        generated_context = generated_contexts[0]
        self.assertDictEqual({**original_context.test_variables,
                              'variable': 1, 'variable_index': 0,
                              'variable2': 'a', 'variable2_index': 0
                              },
                             generated_context.test_variables)
        self.assertDictEqual(original_context.stage_variables, generated_context.stage_variables)
        self.assertDictEqual(original_context.secrets, generated_context.secrets)

        generated_context = generated_contexts[1]
        self.assertDictEqual({**original_context.test_variables,
                              'variable': 1, 'variable_index': 0,
                              'variable2': 'b', 'variable2_index': 1
                              },
                             generated_context.test_variables)
        self.assertDictEqual(original_context.stage_variables, generated_context.stage_variables)
        self.assertDictEqual(original_context.secrets, generated_context.secrets)

        generated_context = generated_contexts[2]
        self.assertDictEqual({**original_context.test_variables,
                              'variable': 2, 'variable_index': 1,
                              'variable2': 'a', 'variable2_index': 0
                              },
                             generated_context.test_variables)
        self.assertDictEqual(original_context.stage_variables, generated_context.stage_variables)
        self.assertDictEqual(original_context.secrets, generated_context.secrets)

        generated_context = generated_contexts[3]
        self.assertDictEqual({**original_context.test_variables,
                              'variable': 2, 'variable_index': 1,
                              'variable2': 'b', 'variable2_index': 1
                              },
                             generated_context.test_variables)
        self.assertDictEqual(original_context.stage_variables, generated_context.stage_variables)
        self.assertDictEqual(original_context.secrets, generated_context.secrets)

    def test_given_empty_context_when_replicate_stage_with_one_variables_then_contexts(self):
        original_context = Context(test_variables={}, stage_variables={}, secrets={})

        generated_contexts = original_context.replicate_on_stage({'variable': [1, 2]})

        self.assertEqual(2, len(generated_contexts))

        contexts_0 = generated_contexts[0]
        self.assertDictEqual(original_context.test_variables, contexts_0.test_variables)
        self.assertDictEqual({**original_context.stage_variables, 'variable': 1, 'variable_index': 0},
                             contexts_0.stage_variables)
        self.assertDictEqual(original_context.secrets, contexts_0.secrets)

        contexts_1 = generated_contexts[1]
        self.assertDictEqual(original_context.test_variables, contexts_1.test_variables)
        self.assertDictEqual({**original_context.stage_variables, 'variable': 2, 'variable_index': 1},
                             contexts_1.stage_variables)
        self.assertDictEqual(original_context.secrets, contexts_1.secrets)

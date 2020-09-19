from folker.model.context import Context


def _compare_contexts(context,
                      expected_test_variables,
                      expected_stage_variables,
                      expected_secrets):
    assert expected_test_variables == context.test_variables
    assert expected_stage_variables == context.stage_variables
    assert expected_secrets == context.secrets


class TestContextReplication:

    def test_given_empty_context_when_no_variables_then_same_context(self):
        original_context = Context(test_variables={},
                                   stage_variables={},
                                   secrets={})

        generated_contexts = original_context.replicate_on_test({})

        assert 1 == len(generated_contexts)
        _compare_contexts(generated_contexts[0],
                          expected_test_variables=original_context.test_variables,
                          expected_stage_variables=original_context.stage_variables,
                          expected_secrets=original_context.secrets)

    def test_given_empty_context_when_replicate_test_with_one_variables_then_contexts(self):
        original_context = Context(test_variables={},
                                   stage_variables={},
                                   secrets={})

        generated_contexts = original_context.replicate_on_test({'variable': [1, 2]})

        assert 2 == len(generated_contexts)

        _compare_contexts(generated_contexts[0],
                          expected_test_variables={**original_context.test_variables,
                                                   'variable': 1,
                                                   'variable_index': 0},
                          expected_stage_variables=original_context.stage_variables,
                          expected_secrets=original_context.secrets)
        _compare_contexts(generated_contexts[1],
                          expected_test_variables={**original_context.test_variables,
                                                   'variable': 2,
                                                   'variable_index': 1},
                          expected_stage_variables=original_context.stage_variables,
                          expected_secrets=original_context.secrets)

    def test_given_empty_context_when_replicate_test_with_two_variables_then_contexts(self):
        original_context = Context(test_variables={}, stage_variables={}, secrets={})

        generated_contexts = original_context.replicate_on_test({'variable': [1, 2],
                                                                 'variable2': ['a', 'b']})

        assert 4 == len(generated_contexts)

        _compare_contexts(generated_contexts[0],
                          expected_test_variables={**original_context.test_variables,
                                                   'variable': 1, 'variable_index': 0,
                                                   'variable2': 'a', 'variable2_index': 0
                                                   },
                          expected_stage_variables=original_context.stage_variables,
                          expected_secrets=original_context.secrets)
        _compare_contexts(generated_contexts[1],
                          expected_test_variables={**original_context.test_variables,
                                                   'variable': 1, 'variable_index': 0,
                                                   'variable2': 'b', 'variable2_index': 1
                                                   },
                          expected_stage_variables=original_context.stage_variables,
                          expected_secrets=original_context.secrets)
        _compare_contexts(generated_contexts[2],
                          expected_test_variables={**original_context.test_variables,
                                                   'variable': 2, 'variable_index': 1,
                                                   'variable2': 'a', 'variable2_index': 0
                                                   },
                          expected_stage_variables=original_context.stage_variables,
                          expected_secrets=original_context.secrets)
        _compare_contexts(generated_contexts[3],
                          expected_test_variables={**original_context.test_variables,
                                                   'variable': 2, 'variable_index': 1,
                                                   'variable2': 'b', 'variable2_index': 1
                                                   },
                          expected_stage_variables=original_context.stage_variables,
                          expected_secrets=original_context.secrets)

    def test_given_not_empty_context_when_replicate_test_with_two_variables_then_contexts(self):
        original_context = Context(test_variables={'test_vble': 'test_value'},
                                   stage_variables={'stage_vble': 'stage_value'},
                                   secrets={'secret_vble': 'secret_value'})

        generated_contexts = original_context.replicate_on_test({'variable': [1, 2],
                                                                 'variable2': ['a', 'b']})

        assert 4 == len(generated_contexts)

        _compare_contexts(generated_contexts[0],
                          expected_test_variables={**original_context.test_variables,
                                                   'variable': 1, 'variable_index': 0,
                                                   'variable2': 'a', 'variable2_index': 0
                                                   },
                          expected_stage_variables=original_context.stage_variables,
                          expected_secrets=original_context.secrets)
        _compare_contexts(generated_contexts[1],
                          expected_test_variables={**original_context.test_variables,
                                                   'variable': 1, 'variable_index': 0,
                                                   'variable2': 'b', 'variable2_index': 1
                                                   },
                          expected_stage_variables=original_context.stage_variables,
                          expected_secrets=original_context.secrets)
        _compare_contexts(generated_contexts[2],
                          expected_test_variables={**original_context.test_variables,
                                                   'variable': 2, 'variable_index': 1,
                                                   'variable2': 'a', 'variable2_index': 0
                                                   },
                          expected_stage_variables=original_context.stage_variables,
                          expected_secrets=original_context.secrets)
        _compare_contexts(generated_contexts[3],
                          expected_test_variables={**original_context.test_variables,
                                                   'variable': 2, 'variable_index': 1,
                                                   'variable2': 'b', 'variable2_index': 1
                                                   },
                          expected_stage_variables=original_context.stage_variables,
                          expected_secrets=original_context.secrets)

    def test_given_empty_context_when_replicate_stage_with_one_variables_then_contexts(self):
        original_context = Context(test_variables={}, stage_variables={}, secrets={})

        generated_contexts = original_context.replicate_on_stage({'variable': [1, 2]})

        assert 2 == len(generated_contexts)

        _compare_contexts(generated_contexts[0],
                          expected_test_variables=original_context.test_variables,
                          expected_stage_variables={**original_context.stage_variables,
                                                    'variable': 1,
                                                    'variable_index': 0},
                          expected_secrets=original_context.secrets)
        _compare_contexts(generated_contexts[1],
                          expected_test_variables=original_context.test_variables,
                          expected_stage_variables={**original_context.stage_variables,
                                                    'variable': 2,
                                                    'variable_index': 1},
                          expected_secrets=original_context.secrets)

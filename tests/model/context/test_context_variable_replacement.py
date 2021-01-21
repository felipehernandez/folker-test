from folker.model.context import Context


class TestContextVariableReplacement:

    def test_given_plain_str_then_same_str(self):
        context = Context(test_variables={},
                          stage_variables={},
                          secrets={})
        result = context.replace_variables('a_str')

        assert result == 'a_str'

    def test_given_str_with_reference_then_resolved_str(self):
        context = Context(test_variables={'ref': 'a_str'},
                          stage_variables={},
                          secrets={})
        result = context.replace_variables('${ref}')

        assert result == 'a_str'

    def test_given_plain_list_then_same_str(self):
        context = Context(test_variables={},
                          stage_variables={},
                          secrets={})
        result = context.replace_variables(['str1', 'str2'])

        assert result == ['str1', 'str2']

    def test_given_list_with_reference_then_resolved_str(self):
        context = Context(test_variables={'ref1': 'str1',
                                          'ref2': 'str2'},
                          stage_variables={},
                          secrets={})
        result = context.replace_variables(['${ref1}', '${ref2}'])

        assert result == ['str1', 'str2']

    def test_given_plain_dict_then_same_str(self):
        context = Context(test_variables={},
                          stage_variables={},
                          secrets={})
        result = context.replace_variables({'key', 'value'})

        assert result == {'key', 'value'}

    def test_given_dict_with_reference_then_resolved_str(self):
        context = Context(test_variables={'ref1': 'str1'},
                          stage_variables={},
                          secrets={})
        result = context.replace_variables({'key': '${ref1}'})

        assert result == {'key': 'str1'}

    def test_given_dict_with_deep_reference_then_resolved_str(self):
        context = Context(test_variables={'ref1': 'str1',
                                          'ref2': 'str2'},
                          stage_variables={},
                          secrets={})
        result = context.replace_variables({'key0': {'key11': '${ref1}',
                                                     'key12': '${ref2}'}
                                            })

        assert result == {'key0': {'key11': 'str1', 'key12': 'str2'}}

from folker.model.context.context import contains_variable_reference, Context


class TestContainsVariableReference:
    def test_complex_object_does_not_contains_variable_reference(self):
        assert [] == contains_variable_reference(Context())

    def test_int_does_not_contains_variable_reference(self):
        assert [] == contains_variable_reference(1)

    def test_dict_does_not_contains_variable_reference(self):
        assert [] == contains_variable_reference({})

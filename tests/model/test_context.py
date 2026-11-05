import collections
import warnings

from folker.model.context.context import contains_variable_reference, Context


class TestContainsVariableReference:
    def test_complex_object_does_not_contains_variable_reference(self):
        assert [] == contains_variable_reference(Context())

    def test_int_does_not_contains_variable_reference(self):
        assert [] == contains_variable_reference(1)

    def test_dict_does_not_contains_variable_reference(self):
        assert [] == contains_variable_reference({})


class TestContextConstructors:
    def test_empty_context(self):
        empty_context = Context.empty_context()

        assert {} == empty_context.stage_variables
        assert {} == empty_context.test_variables
        assert {} == empty_context.secrets

    def test_complete_stage(self):
        dirty_context = Context(secrets={'k1': 'v1'},
                                test_variables={'k2': 'v2'},
                                stage_variables={'k3': 'v3'})

        dirty_context.finalise_stage()

        assert dirty_context.secrets == {'k1': 'v1'}
        assert dirty_context.test_variables == {'k2': 'v2'}
        assert dirty_context.stage_variables == {}


class TestContextSave:
    def test_complex_save(self):
        context = Context(secrets={},
                          test_variables={},
                          stage_variables={'k1': {'k2': {'k3': 'value'}}})

        context.save_on_stage('k1.k2.k4', 'new_value')

        assert context.stage_variables == {'k1': {'k2': {'k3': 'value', 'k4': 'new_value'}}}

    def test_nested_save_merges_without_deprecated_collections_api(self, monkeypatch):
        # BUG-01: merging into an existing nested dict used collections.Mapping,
        # removed in Python 3.10 (DeprecationWarning on 3.9, AttributeError on 3.10+).
        # On 3.9 the alias is cached after first access, so drop it to make the
        # check independent of test order and Python version.
        monkeypatch.delattr(collections, 'Mapping', raising=False)
        context = Context.empty_context()

        with warnings.catch_warnings():
            warnings.simplefilter('error', DeprecationWarning)
            context.save_on_test('a.b.c', 1)
            context.save_on_test('a.b.d', 2)

        assert context.test_variables == {'a': {'b': {'c': 1, 'd': 2}}}

    def test_complex_save_override(self):
        context = Context(secrets={},
                          test_variables={},
                          stage_variables={'k1': {'k2': {'k3': 'value'}}})

        context.save_on_stage('k1.k2.k3', 'new_value')

        assert context.stage_variables == {'k1': {'k2': {'k3': 'new_value'}}}

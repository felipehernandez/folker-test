import collections
from copy import deepcopy

from folker.model.error.variables import VariableReferenceResolutionException
from folker.util.variable import contains_variable_reference


def _resolve_variable_reference(context: dict, path: str) -> str:
    path_steps = path.split('.')

    context_navigation = context
    try:
        for step in path_steps:
            if '[' in step:
                step = int(step[1:-1])
            try:
                context_navigation = context_navigation[step]
            except:
                context_navigation = getattr(context_navigation, step)
    except:
        raise VariableReferenceResolutionException(variable_reference=path)

    return context_navigation


class Context:
    test_variables: dict
    stage_variables: dict
    secrets: dict

    def __init__(self,
                 test_variables: dict = None,
                 stage_variables: dict = None,
                 secrets: dict = None) -> None:
        super().__init__()

        if test_variables is None:
            self.test_variables = {}
        else:
            self.test_variables = deepcopy(test_variables)

        if stage_variables is None:
            self.stage_variables = {}
        else:
            self.stage_variables = deepcopy(stage_variables)

        if secrets is None:
            self.secrets = {}
        else:
            self.secrets = deepcopy(secrets)

    def __copy__(self):
        return deepcopy(self)

    def replicate_on_test(self, variables: dict):
        contexts = self._replicate_on_context(self.test_variables, variables)

        generated_contexts = []
        for context in contexts:
            new_context = self.__copy__()
            new_context.test_variables = context
            generated_contexts.append(new_context)

        return generated_contexts

    def replicate_on_stage(self, variables: dict):
        contexts = self._replicate_on_context(self.stage_variables, variables)

        generated_contexts = []
        for context in contexts:
            # Test variables and secrets references are kept because we want each stage
            # to store on the same test and secret variables
            generated_contexts.append(Context(test_variables=self.test_variables,
                                              stage_variables=context,
                                              secrets=self.secrets))

        return generated_contexts

    def _replicate_on_context(self, context: dict, variables: dict):
        replicated_contexts = [context]

        if len(variables) == 0:
            return replicated_contexts

        for key in reversed(list(variables.keys())):
            new_contexts = []
            values = variables.get(key)
            if isinstance(values, str):
                values = self.extract_value_from_context(values)
                if isinstance(values, str):
                    values = [values]
            for index, value in enumerate(values):
                for base_context in [{**context} for context in replicated_contexts]:
                    new_contexts.append({
                        **base_context,
                        key: value,
                        key + '_index': index
                    })
            replicated_contexts = new_contexts

        return replicated_contexts

    def extract_value_from_context(self, reference):
        if not isinstance(reference, str):
            return reference
        context_value = contains_variable_reference(reference)
        if len(context_value) == 0:
            return reference

        return self.resolve_variable_reference(context_value[0])

    def resolve_variable_reference(self, variable_reference: str) -> str:
        try:
            return _resolve_variable_reference(self.stage_variables, variable_reference)
        except VariableReferenceResolutionException:
            pass
        try:
            return _resolve_variable_reference(self.test_variables, variable_reference)
        except VariableReferenceResolutionException:
            pass
        return _resolve_variable_reference(self.secrets, variable_reference)

    def replace_variables(self, object):
        if type(object) is str:
            return self._replace_variables(object)
        elif type(object) is list:
            return [self.replace_variables(value) for value in object]
        elif type(object) is dict:
            for key, value in object.items():
                object[key] = self.replace_variables(value)
            return object
        else:
            return object

    def _replace_variables(self, text):
        references = contains_variable_reference(text)
        for reference in references:
            value = self.resolve_variable_reference(variable_reference=reference)
            if text == '${' + reference + '}':
                text = value
            else:
                text = text.replace('${' + reference + '}', str(value))
        return text

    def map_variables(self, text) -> (str, dict):
        references = contains_variable_reference(text)
        variables = {}
        for reference in references:
            value = self.resolve_variable_reference(variable_reference=reference)
            variables[reference] = value
            text = text.replace('${' + reference + '}', 'variables["' + str(reference) + '"]')

        return text, variables

    def save_on_test(self, variable, value):
        variable_children = variable.split('.')

        if len(variable_children) == 1:
            self.test_variables[variable] = value
            return

        variable_root = variable_children[0]
        variable_value = {variable_children[-1]: value}
        path = variable_children[1:-1]
        for element in reversed(path):
            variable_value = {element: variable_value}

        self.test_variables[variable_root] = self._merge_dictionaries(self.test_variables.get(variable_root, {}), variable_value)

    def _merge_dictionaries(self, stable: dict, new_values: dict):
        if len(new_values) == 0:
            return stable
        for k, v in new_values.items():
            if (k in stable and isinstance(stable[k], dict)
                    and isinstance(new_values[k], collections.Mapping)):
                self._merge_dictionaries(stable[k], new_values[k])
            else:
                stable[k] = new_values[k]
        return stable

    def save_on_stage(self, variable, value):
        variable_children = variable.split('.')

        if len(variable_children) == 1:
            self.stage_variables[variable] = value
            return

        variable_root = variable_children[0]
        variable_value = {variable_children[-1]: value}
        path = variable_children[1:-1]
        for element in reversed(path):
            variable_value = {element: variable_value}

        self.stage_variables[variable_root] = self._merge_dictionaries(self.stage_variables.get(variable_root, {}), variable_value)

    def end_stage(self):
        self.stage_variables = {}


def EMPTY_CONTEXT():
    return Context({}, {}, {})

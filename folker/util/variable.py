import re

from folker.model.error.variables import VariableReferenceResolutionException


def contains_variable_reference(text):
    if not isinstance(text, str):
        return []
    return re.findall('\${([^{}]+)}', text)


def replace_variables(test_context: dict, stage_context: dict, text):
    references = contains_variable_reference(text)
    for reference in references:
        value = resolve_variable_reference(test_context=test_context, stage_context=stage_context, variable_reference=reference)
        text = text.replace('${' + reference + '}', str(value))
    return text


def resolve_variable_reference(test_context: dict, stage_context: dict, variable_reference: str) -> str:
    stage_value = _resolve_variable_reference(stage_context, variable_reference)
    if stage_value is not None:
        return stage_value

    test_value = _resolve_variable_reference(test_context, variable_reference)

    if test_value is not None:
        return test_value

    raise VariableReferenceResolutionException(variable_reference=variable_reference)


def map_variables(test_context: dict, stage_context: dict, text) -> (str, dict):
    references = contains_variable_reference(text)
    variables = {}
    for reference in references:
        value = resolve_variable_reference(test_context=test_context, stage_context=stage_context, variable_reference=reference)
        variables[reference] = value
        text = text.replace('${' + reference + '}', 'variables["' + str(reference) + '"]')

    return text, variables


def _resolve_variable_reference(context: dict, path: str) -> str:
    path_steps = path.split('.')

    context_navigation = context
    try:
        for step in path_steps:
            if '[' in step:
                step = int(step[1:-1])
            context_navigation = context_navigation[step]
    except:
        return None

    return context_navigation


def recursive_replace_variables(test_context: dict, stage_context: dict, object):
    if type(object) is str:
        return replace_variables(test_context, stage_context, object)
    elif type(object) is list:
        return [recursive_replace_variables(test_context, stage_context, value) for value in object]
    elif type(object) is dict:
        for key, value in object.items():
            object[key] = recursive_replace_variables(test_context, stage_context, value)
        return object
    else:
        return object


def extract_value_from_cntext(test_context: dict, stage_context: dict, text):
    if not isinstance(text, str):
        return text
    reference = contains_variable_reference(text)
    if len(reference) == 0:
        return text

    return resolve_variable_reference(test_context, stage_context, reference[0])

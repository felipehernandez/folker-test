import sys

import pytest

from folker.model import Context
from folker.module.code.action import CodeStageAction

MODULE = '''
calls = []

def concat(first, second):
    return f'{first} - {second}'

def as_dict(first, second):
    return {'first': first, 'second': second}

def nothing():
    return None

def record(**kwargs):
    calls.append(kwargs)
    return len(calls)

def fail(**kwargs):
    raise ValueError('failed on purpose')
'''


@pytest.fixture
def code_module(tmp_path, monkeypatch):
    """A module in the working directory, as `testcode.code_example` in the integration image"""
    name = f'folker_code_action_probe_{id(tmp_path)}'
    (tmp_path / f'{name}.py').write_text(MODULE)
    monkeypatch.syspath_prepend(str(tmp_path))
    yield name
    sys.modules.pop(name, None)


def execute(logger, module, method, parameters=None, context=None):
    action = CodeStageAction(module=module, method=method, parameters=parameters)
    return action.execute(logger=logger, context=context or Context())


@pytest.mark.action_code
class TestCodeActionExecution:
    def test_the_method_is_called_with_the_parameters_and_its_result_saved(
            self, code_module, plain_console_test_logger_on_trace):
        context = execute(plain_console_test_logger_on_trace, code_module, 'concat',
                          {'first': 'hello', 'second': 'world'})

        assert context.stage_variables['result'] == 'hello - world'
        assert 'elapsed_time' in context.stage_variables

    def test_a_dict_result_is_saved_as_is(self, code_module, plain_console_test_logger_on_trace):
        context = execute(plain_console_test_logger_on_trace, code_module, 'as_dict',
                          {'first': 1, 'second': [2, 3]})

        assert context.stage_variables['result'] == {'first': 1, 'second': [2, 3]}

    def test_a_method_returning_nothing_saves_none(self, code_module,
                                                   plain_console_test_logger_on_trace):
        context = execute(plain_console_test_logger_on_trace, code_module, 'nothing')

        assert context.stage_variables['result'] is None

    def test_variables_in_the_parameters_are_resolved(self, code_module,
                                                      plain_console_test_logger_on_trace):
        context = Context(test_variables={'name': 'folker'}, secrets={'token': 'abc'})

        result = execute(plain_console_test_logger_on_trace, code_module, 'concat',
                         {'first': 'hi ${name}', 'second': '${token}'}, context)

        assert result.stage_variables['result'] == 'hi folker - abc'

    def test_the_action_is_not_changed_by_resolving_variables(
            self, code_module, plain_console_test_logger_on_trace):
        action = CodeStageAction(module=code_module, method='concat',
                                 parameters={'first': '${name}', 'second': 'x'})

        action.execute(logger=plain_console_test_logger_on_trace,
                       context=Context(test_variables={'name': 'folker'}))

        assert action.parameters == {'first': '${name}', 'second': 'x'}

    def test_the_module_is_imported_once_and_shared_between_calls(
            self, code_module, plain_console_test_logger_on_trace):
        first = execute(plain_console_test_logger_on_trace, code_module, 'record', {'n': 1})
        second = execute(plain_console_test_logger_on_trace, code_module, 'record', {'n': 2})

        assert (first.stage_variables['result'], second.stage_variables['result']) == (1, 2)

    # There is no error handling: any failure ends the test through the stage
    def test_a_module_that_does_not_exist_raises(self, plain_console_test_logger_on_trace):
        with pytest.raises(ModuleNotFoundError):
            execute(plain_console_test_logger_on_trace, 'folker_no_such_module', 'method')

    def test_a_method_that_does_not_exist_raises(self, code_module,
                                                 plain_console_test_logger_on_trace):
        with pytest.raises(AttributeError):
            execute(plain_console_test_logger_on_trace, code_module, 'no_such_method')

    def test_an_exception_from_the_method_propagates(self, code_module,
                                                     plain_console_test_logger_on_trace):
        with pytest.raises(ValueError, match='failed on purpose'):
            execute(plain_console_test_logger_on_trace, code_module, 'fail')

    def test_parameters_that_do_not_match_the_method_raise(self, code_module,
                                                           plain_console_test_logger_on_trace):
        with pytest.raises(TypeError):
            execute(plain_console_test_logger_on_trace, code_module, 'concat', {'first': 'only'})

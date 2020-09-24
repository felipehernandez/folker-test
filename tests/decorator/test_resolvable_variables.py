from folker.decorator import resolvable_variables
from folker.model import Context
from folker.module.void.action import VoidStageAction


def test_resolve_variables(mocker):
    value_reference = 'value_reference'
    resolved_value = 'new_value'

    @resolvable_variables
    def called_method(self, *args, **kargs):
        assert resolved_value == self.key
        return kargs['context']

    action = VoidStageAction()
    action.key = '${' + value_reference + '}'

    original_context = Context({value_reference: resolved_value})

    result = called_method(self=action, context=original_context)

    assert original_context == result
    assert '${' + value_reference + '}' == action.key

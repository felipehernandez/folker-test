from folker.decorator import resolvable_variables
from folker.module.void.action import VoidAction


def test_resolve_variables(mocker):
    execution_result = 'Context'
    original_attribute_value = 'old_value'
    variable_resolved_attribute_value = 'new_value'

    @resolvable_variables
    def called_method(self, *args, **kargs):
        assert variable_resolved_attribute_value == self.new_key
        return execution_result

    action = VoidAction()
    action.new_key = original_attribute_value

    original_context = mocker.patch('folker.model.Context')
    original_context.replace_variables.return_value = variable_resolved_attribute_value

    result = called_method(self=action, context=original_context)

    assert execution_result == result
    assert original_attribute_value == action.new_key

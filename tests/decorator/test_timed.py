from folker.decorator import timed_action
from folker.model import Context


def test_timed_action(mocker):
    mocker.patch('folker.decorator.timed.time', side_effect=[1, 2])

    @timed_action
    def called_method(self, *args, **kargs):
        return kargs['context']

    original_context = Context()

    result = called_method(self=None, context=original_context)

    assert 1000 == original_context.stage_variables.get('elapsed_time')
    assert original_context == result

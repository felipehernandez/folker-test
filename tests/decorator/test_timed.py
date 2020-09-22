from folker.decorator import timed_action


def test_timed_action(mocker):
    mocker.patch('folker.decorator.timed.time', side_effect=[1, 2])

    @timed_action
    def called_method(self, *args, **kargs):
        return kargs['context']

    original_context = mocker.patch('folker.model.Context')
    spy_save_on_stage = mocker.spy(original_context, 'save_on_stage')

    result = called_method(self=None, context=original_context)

    spy_save_on_stage.assert_called_once_with('elapsed_time', 1000)
    assert original_context == result

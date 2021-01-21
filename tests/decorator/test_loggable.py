from folker.decorator import loggable_action
from folker.model import Context
from folker.module.void.action import VoidStageAction


def test_loggable_when_trace(mocker):
    returned_context = 'Context'

    @loggable_action
    def called_method(self, *args, **kargs):
        return returned_context

    action = VoidStageAction()
    original_context = Context()
    mock_test_logger = mocker.patch('folker.logger.TestLogger')

    spy_log_prelude = mocker.spy(mock_test_logger, 'action_prelude')
    spy_log_conclusion = mocker.spy(mock_test_logger, 'action_conclusion')
    mocker.patch('folker.decorator.loggable.is_trace', return_value=True)

    result = called_method(self=action,
                           logger=mock_test_logger,
                           context=original_context)

    spy_log_prelude.assert_called_once_with(action=action.__dict__, context=original_context)
    spy_log_conclusion.assert_called_once_with(action=action.__dict__, context=returned_context)
    assert 'Context' == result


def test_loggable_when_not_trace(mocker):
    returned_context = 'Context'

    @loggable_action
    def called_method(self, *args, **kargs):
        return returned_context

    action = VoidStageAction()
    original_context = Context()
    mock_test_logger = mocker.patch('folker.logger.TestLogger')

    spy_log_prelude = mocker.spy(mock_test_logger, 'action_prelude')
    spy_log_conclusion = mocker.spy(mock_test_logger, 'action_conclusion')
    mocker.patch('folker.decorator.loggable.is_trace', return_value=False)

    result = called_method(self=action,
                           logger=mock_test_logger,
                           context=original_context)

    spy_log_prelude.assert_not_called()
    spy_log_conclusion.assert_not_called()
    assert 'Context' == result

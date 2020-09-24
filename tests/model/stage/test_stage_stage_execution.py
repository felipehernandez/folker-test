import pytest

from folker.model import Stage, Context
from folker.model.error import TestFailException, \
    MalformedAssertionException, \
    UnresolvableAssertionException, \
    SourceException


def mock_response(expected, return_value):
    return (lambda logger, context:
            return_value
            if context.replace_variables('${key}') == expected
            else None)


def test_stage_success(mocker):
    mocked_action = mocker.patch('folker.model.stage.StageAction')
    mocked_save = mocker.patch('folker.model.stage.StageSave')
    mocked_log = mocker.patch('folker.model.stage.StageLog')
    mocked_assertions = mocker.patch('folker.model.stage.StageAssertions')

    stage = Stage()
    stage.action = mocked_action
    stage.save = mocked_save
    stage.log = mocked_log
    stage.assertions = mocked_assertions

    mocked_logger = mocker.patch('folker.logger.TestLogger')
    initial_context = Context({'key': 'initial'})
    asserted_context = Context({'key': 'asserted'})

    mocked_action.execute.side_effect = mock_response('initial', Context({'key': 'actioned'}))
    mocked_save.execute.side_effect = mock_response('actioned', Context({'key': 'saved'}))
    mocked_log.execute.side_effect = mock_response('saved', Context({'key': 'logged'}))
    mocked_assertions.execute.side_effect = mock_response('logged', asserted_context)

    result = stage.execute(logger=mocked_logger, context=initial_context)

    assert result.secrets == asserted_context.secrets
    assert result.test_variables == asserted_context.test_variables
    assert result.stage_variables == asserted_context.stage_variables


def test_stage_fail(mocker):
    mocked_action = mocker.patch('folker.model.stage.StageAction')
    mocked_save = mocker.patch('folker.model.stage.StageSave')
    mocked_log = mocker.patch('folker.model.stage.StageLog')
    mocked_assertions = mocker.patch('folker.model.stage.StageAssertions')

    stage = Stage()
    stage.action = mocked_action
    stage.save = mocked_save
    stage.log = mocked_log
    stage.assertions = mocked_assertions

    mocked_logger = mocker.patch('folker.logger.TestLogger')
    initial_context = Context({'key': 'initial'})

    mocked_action.execute.side_effect = mock_response('initial', Context({'key': 'actioned'}))
    mocked_save.execute.side_effect = mock_response('actioned', Context({'key': 'saved'}))
    mocked_log.execute.side_effect = mock_response('saved', Context({'key': 'logged'}))
    mocked_assertions.execute.side_effect = TestFailException(failure_messages=['failure'])

    with pytest.raises(TestFailException) as test_fail_exception:
        stage.execute(logger=mocked_logger, context=initial_context)

        assert test_fail_exception.failure_messages == ['failure']


def test_stage_foreach(mocker):
    mocked_action = mocker.patch('folker.model.stage.StageAction')
    mocked_save = mocker.patch('folker.model.stage.StageSave')
    mocked_log = mocker.patch('folker.model.stage.StageLog')
    mocked_assertions = mocker.patch('folker.model.stage.StageAssertions')

    stage = Stage()
    stage.action = mocked_action
    stage.save = mocked_save
    stage.log = mocked_log
    stage.assertions = mocked_assertions
    stage.foreach = {'element': ['a', 'b']}

    mocked_logger = mocker.patch('folker.logger.TestLogger')
    initial_context = Context({})

    def action_side_effect(logger, context):
        value = context.replace_variables('${element}')
        index = context.replace_variables('${element_index}')
        context.save_on_test(str(index), value)
        return context

    mocked_action.execute.side_effect = action_side_effect
    mocked_save.execute.side_effect = (lambda logger, context: context)
    mocked_log.execute.side_effect = (lambda logger, context: context)
    mocked_assertions.execute.side_effect = (lambda logger, context: context)

    result = stage.execute(logger=mocked_logger, context=initial_context)

    assert result.secrets == {}
    assert result.test_variables == {'0': 'a', '1': 'b'}
    assert result.stage_variables == {}


def test_stage_conditional_execution_true(mocker):
    mocked_action = mocker.patch('folker.model.stage.StageAction')
    mocked_save = mocker.patch('folker.model.stage.StageSave')
    mocked_log = mocker.patch('folker.model.stage.StageLog')
    mocked_assertions = mocker.patch('folker.model.stage.StageAssertions')

    stage = Stage()
    stage.action = mocked_action
    stage.save = mocked_save
    stage.log = mocked_log
    stage.assertions = mocked_assertions
    stage.condition = 'True'

    mocked_logger = mocker.patch('folker.logger.TestLogger')
    initial_context = Context({'key': 'initial'})
    asserted_context = Context({'key': 'asserted'})

    mocked_action.execute.side_effect = mock_response('initial', Context({'key': 'actioned'}))
    mocked_save.execute.side_effect = mock_response('actioned', Context({'key': 'saved'}))
    mocked_log.execute.side_effect = mock_response('saved', Context({'key': 'logged'}))
    mocked_assertions.execute.side_effect = mock_response('logged', asserted_context)

    result = stage.execute(logger=mocked_logger, context=initial_context)

    assert result.secrets == asserted_context.secrets
    assert result.test_variables == asserted_context.test_variables
    assert result.stage_variables == asserted_context.stage_variables


def test_stage_conditional_execution_false(mocker):
    mocked_action = mocker.patch('folker.model.stage.StageAction')
    mocked_save = mocker.patch('folker.model.stage.StageSave')
    mocked_log = mocker.patch('folker.model.stage.StageLog')
    mocked_assertions = mocker.patch('folker.model.stage.StageAssertions')

    stage = Stage()
    stage.action = mocked_action
    stage.save = mocked_save
    stage.log = mocked_log
    stage.assertions = mocked_assertions
    stage.condition = 'False'

    mocked_logger = mocker.patch('folker.logger.TestLogger')
    initial_context = Context({'key': 'initial'})
    asserted_context = Context({'key': 'asserted'})

    mocked_action.execute.side_effect = mock_response('initial', Context({'key': 'actioned'}))
    mocked_save.execute.side_effect = mock_response('actioned', Context({'key': 'saved'}))
    mocked_log.execute.side_effect = mock_response('saved', Context({'key': 'logged'}))
    mocked_assertions.execute.side_effect = mock_response('logged', asserted_context)

    result = stage.execute(logger=mocked_logger, context=initial_context)

    assert result.secrets == initial_context.secrets
    assert result.test_variables == initial_context.test_variables
    assert result.stage_variables == initial_context.stage_variables


def test_stage_error_from_action(mocker):
    mocked_action = mocker.patch('folker.model.stage.StageAction')

    stage = Stage()
    stage.action = mocked_action

    mocked_logger = mocker.patch('folker.logger.TestLogger')
    initial_context = Context({'key': 'initial'})

    mocked_action.execute.side_effect = SourceException()

    with pytest.raises(SourceException) as raised_exception:
        stage.execute(logger=mocked_logger, context=initial_context)

        assert raised_exception.details['stage'] == stage


def test_stage_unresolvable_assertion_exception_from_assertions(mocker):
    mocked_action = mocker.patch('folker.model.stage.StageAction')
    mocked_save = mocker.patch('folker.model.stage.StageSave')
    mocked_log = mocker.patch('folker.model.stage.StageLog')
    mocked_assertions = mocker.patch('folker.model.stage.StageAssertions')

    stage = Stage()
    stage.action = mocked_action
    stage.save = mocked_save
    stage.log = mocked_log
    stage.assertions = mocked_assertions

    mocked_logger = mocker.patch('folker.logger.TestLogger')
    initial_context = Context({'key': 'initial'})

    mocked_action.execute.side_effect = mock_response('initial', Context({'key': 'actioned'}))
    mocked_save.execute.side_effect = mock_response('actioned', Context({'key': 'saved'}))
    mocked_log.execute.side_effect = mock_response('saved', Context({'key': 'logged'}))
    mocked_assertions.execute.side_effect = \
        UnresolvableAssertionException(assertion='unresolvable_assertion')

    with pytest.raises(UnresolvableAssertionException) as raised_exception:
        stage.execute(logger=mocked_logger, context=initial_context)

        assert raised_exception.assertion == 'malformed_assertion'


def test_stage_malformed_assertion_exception_from_assertions(mocker):
    mocked_action = mocker.patch('folker.model.stage.StageAction')
    mocked_save = mocker.patch('folker.model.stage.StageSave')
    mocked_log = mocker.patch('folker.model.stage.StageLog')
    mocked_assertions = mocker.patch('folker.model.stage.StageAssertions')

    stage = Stage()
    stage.action = mocked_action
    stage.save = mocked_save
    stage.log = mocked_log
    stage.assertions = mocked_assertions

    mocked_logger = mocker.patch('folker.logger.TestLogger')
    initial_context = Context({'key': 'initial'})

    mocked_action.execute.side_effect = mock_response('initial', Context({'key': 'actioned'}))
    mocked_save.execute.side_effect = mock_response('actioned', Context({'key': 'saved'}))
    mocked_log.execute.side_effect = mock_response('saved', Context({'key': 'logged'}))
    mocked_assertions.execute.side_effect = \
        MalformedAssertionException(assertion='malformed_assertion')

    with pytest.raises(MalformedAssertionException) as raised_exception:
        stage.execute(logger=mocked_logger, context=initial_context)

        assert raised_exception.assertion == 'malformed_assertion'

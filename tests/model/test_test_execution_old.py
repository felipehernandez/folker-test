from unittest.mock import call

from folker.model import Test, Context
from folker.model.error import SourceException


def test_test_execution_simple_success_scenario(mocker):
    mocked_stage = mocker.patch('folker.model.stage.Stage')
    mocked_logger = mocker.patch('folker.logger.TestLogger')

    test = Test()
    test.stages = [mocked_stage]

    mocked_stage.execute.return_value = Context({'key': 'stage_completed'})

    result = test.execute(mocked_logger, Context({'key': 'initial'}))

    assert result
    assert mocked_stage.execute.mock_calls == [call(mocked_logger, Context({'key': 'initial'}))]


def test_test_execution_simple_success_scenario_missing_context(mocker):
    mocked_stage = mocker.patch('folker.model.stage.Stage')
    mocked_logger = mocker.patch('folker.logger.TestLogger')

    test = Test()
    test.stages = [mocked_stage]

    mocked_stage.execute.return_value = Context({'key': 'stage_completed'})

    result = test.execute(mocked_logger, None)

    assert result
    assert mocked_stage.execute.mock_calls == [call(mocked_logger, Context())]


def test_test_execution_simple_failure_scenario(mocker):
    mocked_stage = mocker.patch('folker.model.stage.Stage')
    mocked_logger = mocker.patch('folker.logger.TestLogger')

    test = Test()
    test.stages = [mocked_stage]

    mocked_stage.execute.side_effect = SourceException()

    result = test.execute(mocked_logger, None)

    assert not result
    assert mocked_stage.execute.mock_calls == [call(mocked_logger, Context())]


def test_test_execution_simple_error_scenario(mocker):
    mocked_stage = mocker.patch('folker.model.stage.Stage')
    mocked_logger = mocker.patch('folker.logger.TestLogger')

    test = Test()
    test.stages = [mocked_stage]

    mocked_stage.execute.side_effect = Exception()

    result = test.execute(mocked_logger, None)

    assert not result
    assert mocked_stage.execute.mock_calls == [call(mocked_logger, Context())]


def test_test_execution_multiple_stage_scenario(mocker):
    mocked_stage_1 = mocker.patch('folker.model.stage.Stage', name='Stage1')
    mocked_stage_2 = mocker.patch('folker.model.stage.Stage', name='Stage2')
    mocked_logger = mocker.patch('folker.logger.TestLogger')

    test = Test()
    test.stages = [mocked_stage_1, mocked_stage_2]

    mocked_stage_1.execute.return_value = Context({'key': 'stage_1_completed'})
    mocked_stage_2.execute.return_value = Context({'key': 'stage_2_completed'})

    result = test.execute(mocked_logger, Context({'key': 'initial'}))

    assert result
    assert mocked_stage_1.execute.mock_calls == [
        call(mocked_logger, Context({'key': 'initial'}))]
    assert mocked_stage_2.execute.mock_calls == [
        call(mocked_logger, Context({'key': 'stage_1_completed'}))]


def test_test_execution_foreach_scenario(mocker):
    mocked_stage = mocker.patch('folker.model.stage.Stage')
    mocked_logger = mocker.patch('folker.logger.TestLogger')

    test = Test()
    test.stages = [mocked_stage]
    test.foreach = {'element': ['a', 'b']}

    mocked_stage.execute.return_value = Context({'key': 'stage_completed'})

    result = test.execute(mocked_logger, Context({'key': 'initial'}))

    assert result
    assert mocked_stage.execute.mock_calls == [
        call(mocked_logger, Context({'key': 'initial', 'element': 'a', 'element_index': 0})),
        call(mocked_logger, Context({'key': 'initial', 'element': 'b', 'element_index': 1}))]


def test_test_execution_foreach_with_failure(mocker):
    mocked_stage = mocker.patch('folker.model.stage.Stage')
    mocked_logger = mocker.patch('folker.logger.TestLogger')

    test = Test()
    test.stages = [mocked_stage]
    test.foreach = {'element': ['a', 'b']}

    mocked_stage.execute.side_effect = [Context({'key': 'stage_completed'}),
                                        SourceException()]

    result = test.execute(mocked_logger, Context({'key': 'initial'}))

    assert not result
    assert mocked_stage.execute.mock_calls == [
        call(mocked_logger, Context({'key': 'initial', 'element': 'a', 'element_index': 0})),
        call(mocked_logger, Context({'key': 'initial', 'element': 'b', 'element_index': 1}))]

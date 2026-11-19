from unittest.mock import call

from folker.logger.test_logger import PlainConsoleSequentialTestLogger
from folker.model import Test, Context
from folker.model.error import SourceException


class TestSimpleExecution:
    def test_simple_execution(self, normal_configuration, do_nothing_stage):
        test = Test(name='test_name',
                    stages=[do_nothing_stage])

        test.execute(logger=PlainConsoleSequentialTestLogger(normal_configuration),
                     context=Context.empty_context())

        assert do_nothing_stage.executions_count == 1

    def test_simple_execution_no_context(self, normal_configuration, do_nothing_stage):
        test = Test(name='test_name',
                    stages=[do_nothing_stage])

        test.execute(logger=PlainConsoleSequentialTestLogger(normal_configuration),
                     context=None)

        assert do_nothing_stage.executions_count == 1
        assert do_nothing_stage.execution_contexts == [Context.empty_context()]


class TestForEachExecution:
    def test_one_key_and_one_value_no_context(self, normal_configuration, do_nothing_stage):
        test = Test(name='test_name',
                    foreach={'key1': ['value1']},
                    stages=[do_nothing_stage])

        test.execute(logger=PlainConsoleSequentialTestLogger(normal_configuration),
                     context=None)

        assert do_nothing_stage.executions_count == 1
        assert do_nothing_stage.execution_contexts == [Context(test_variables={'key1': 'value1',
                                                                               'key1_index': 0})]

    def test_one_key_and_one_value(self, normal_configuration, do_nothing_stage):
        test = Test(name='test_name',
                    foreach={'key1': ['value1']},
                    stages=[do_nothing_stage])

        test.execute(logger=PlainConsoleSequentialTestLogger(normal_configuration),
                     context=Context.empty_context())

        assert do_nothing_stage.executions_count == 1

    def test_one_key_and_one_value_context(self, normal_configuration, do_nothing_stage):
        test = Test(name='test_name',
                    foreach={'key1': ['value1']},
                    stages=[do_nothing_stage])

        test.execute(logger=PlainConsoleSequentialTestLogger(normal_configuration),
                     context=Context.empty_context())

        assert any(execution_context == Context(test_variables={'key1': 'value1', 'key1_index': 0})
                   for execution_context in do_nothing_stage.execution_contexts)

    def test_one_key_and_multiple_value(self, normal_configuration, do_nothing_stage):
        test = Test(name='test_name',
                    foreach={'key1': ['value1', 'value2']},
                    stages=[do_nothing_stage])

        test.execute(logger=PlainConsoleSequentialTestLogger(normal_configuration),
                     context=Context.empty_context())

        assert do_nothing_stage.executions_count == 2

    def test_one_key_and_multiple_value_context(self, normal_configuration, do_nothing_stage):
        test = Test(name='test_name',
                    foreach={'key1': ['value1', 'value2']},
                    stages=[do_nothing_stage])

        test.execute(logger=PlainConsoleSequentialTestLogger(normal_configuration),
                     context=Context.empty_context())

        assert any(execution_context == Context(test_variables={'key1': 'value1', 'key1_index': 0})
                   for execution_context in do_nothing_stage.execution_contexts)
        assert any(execution_context == Context(test_variables={'key1': 'value2', 'key1_index': 1})
                   for execution_context in do_nothing_stage.execution_contexts)

    def test_multiple_key_and_one_value(self, normal_configuration, do_nothing_stage):
        test = Test(name='test_name',
                    foreach={'key1': ['value11'], 'key2': ['value21']},
                    stages=[do_nothing_stage])

        test.execute(logger=PlainConsoleSequentialTestLogger(normal_configuration),
                     context=Context.empty_context())

        assert do_nothing_stage.executions_count == 1

    def test_multiple_key_and_one_value_context(self, normal_configuration, do_nothing_stage):
        test = Test(name='test_name',
                    foreach={'key1': ['value11'], 'key2': ['value21']},
                    stages=[do_nothing_stage])

        test.execute(logger=PlainConsoleSequentialTestLogger(normal_configuration),
                     context=Context.empty_context())

        expected_test_variables = {'key1': 'value11', 'key1_index': 0,
                                   'key2': 'value21', 'key2_index': 0}
        assert any(execution_context == Context(test_variables=expected_test_variables)
                   for execution_context in do_nothing_stage.execution_contexts)

    def test_multiple_key_and_multiple_value(self, normal_configuration, do_nothing_stage):
        test = Test(name='test_name',
                    foreach={'key1': ['value11', 'value12'], 'key2': ['value21', 'value22']},
                    stages=[do_nothing_stage])

        test.execute(logger=PlainConsoleSequentialTestLogger(normal_configuration),
                     context=Context.empty_context())

        assert do_nothing_stage.executions_count == 4

    def test_multiple_key_and_multiple_value_context(self, normal_configuration, do_nothing_stage):
        test = Test(name='test_name',
                    foreach={'key1': ['value11', 'value12'], 'key2': ['value21', 'value22']},
                    stages=[do_nothing_stage])

        test.execute(logger=PlainConsoleSequentialTestLogger(normal_configuration),
                     context=Context.empty_context())

        expected_test_variables = [
            {'key1': 'value11', 'key1_index': 0, 'key2': 'value21', 'key2_index': 0},
            {'key1': 'value12', 'key1_index': 1, 'key2': 'value21', 'key2_index': 0},
            {'key1': 'value11', 'key1_index': 0, 'key2': 'value22', 'key2_index': 1},
            {'key1': 'value12', 'key1_index': 1, 'key2': 'value22', 'key2_index': 1}
        ]
        for expected_context in expected_test_variables:
            assert any(execution_context == Context(test_variables=expected_context)
                       for execution_context in do_nothing_stage.execution_contexts)


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


# BUG-03: `executions_result and self._execute(...)` short-circuited after the first failing
# iteration, so the remaining iterations never ran and never reported.
def test_test_execution_foreach_failure_in_first_iteration_runs_the_rest(mocker):
    mocked_stage = mocker.patch('folker.model.stage.Stage')
    mocked_logger = mocker.patch('folker.logger.TestLogger')

    test = Test()
    test.stages = [mocked_stage]
    test.foreach = {'element': ['a', 'b', 'c']}

    mocked_stage.execute.side_effect = [SourceException(),
                                        Context({'key': 'stage_completed'}),
                                        Context({'key': 'stage_completed'})]

    result = test.execute(mocked_logger, Context({'key': 'initial'}))

    assert not result
    assert mocked_stage.execute.mock_calls == [
        call(mocked_logger, Context({'key': 'initial', 'element': 'a', 'element_index': 0})),
        call(mocked_logger, Context({'key': 'initial', 'element': 'b', 'element_index': 1})),
        call(mocked_logger, Context({'key': 'initial', 'element': 'c', 'element_index': 2}))]


def test_test_execution_foreach_reports_every_iteration(mocker):
    mocked_stage = mocker.patch('folker.model.stage.Stage')
    mocked_logger = mocker.patch('folker.logger.TestLogger')

    test = Test()
    test.stages = [mocked_stage]
    test.foreach = {'element': ['a', 'b', 'c']}

    mocked_stage.execute.side_effect = [Exception('first'),
                                        Context({'key': 'stage_completed'}),
                                        SourceException()]

    result = test.execute(mocked_logger, Context({'key': 'initial'}))

    assert not result
    assert mocked_logger.test_start.call_count == 3
    assert mocked_logger.test_finish_error.call_count == 2
    assert mocked_logger.test_finish.call_count == 1


def test_test_execution_foreach_all_iterations_succeed(mocker):
    mocked_stage = mocker.patch('folker.model.stage.Stage')
    mocked_logger = mocker.patch('folker.logger.TestLogger')

    test = Test()
    test.stages = [mocked_stage]
    test.foreach = {'element': ['a', 'b', 'c']}

    mocked_stage.execute.return_value = Context({'key': 'stage_completed'})

    result = test.execute(mocked_logger, Context({'key': 'initial'}))

    assert result
    assert mocked_stage.execute.call_count == 3
    assert mocked_logger.test_finish_error.call_count == 0

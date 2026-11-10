import multiprocessing

import pytest

import folker
from folker.executor import ParallelExecutor
from folker.model import Profile, Stage
from folker.model import Test as FolkerTest  # not `Test`: pytest would try to collect it
from folker.parameters import Configuration
from tests.executor.stages import FailOnValueStage, FailStage, PassStage, SleepStage

START_METHODS = ['fork', 'spawn', 'forkserver']


class RequireGreetingStage(Stage):
    """Fails unless the variable `greeting` is in the context. Module level, so workers can unpickle it."""

    def execute(self, logger, context):
        context.resolve_variable_reference('greeting')
        return context


class ExpectGreetingStage(Stage):
    def __init__(self, expected=None, **kwargs):
        super().__init__(**kwargs)
        self.expected = expected

    def execute(self, logger, context):
        assert context.resolve_variable_reference('greeting') == self.expected
        return context


@pytest.fixture()
def start_method(request, monkeypatch):
    """Make ParallelExecutor's pool use the given start method, without touching global state."""
    method = request.param
    if method not in multiprocessing.get_all_start_methods():
        pytest.skip(f'start method {method} is not available on this platform')

    context = multiprocessing.get_context(method)
    monkeypatch.setattr('folker.executor.parallel_executor.Pool', context.Pool)
    return method


def _tests():
    return [FolkerTest(name=f'test_{i}', stages=[RequireGreetingStage(name='stage')]) for i in range(2)]


@pytest.mark.parametrize('start_method', START_METHODS, indirect=True)
class TestParallelExecutorProfile:
    def test_selected_profile_reaches_the_workers(self, start_method, monkeypatch):
        # BUG-02: workers read the global folker.profiles, which is empty under spawn/forkserver
        monkeypatch.setitem(folker.profiles, 'profile',
                            Profile(name='profile', context={'greeting': 'hello'}))

        success, failures = ParallelExecutor().execute(Configuration(profiles={'profile'}), _tests())

        assert (success, failures) == (['test_0', 'test_1'], [])

    def test_merged_profiles_reach_the_workers(self, start_method, monkeypatch):
        monkeypatch.setitem(folker.profiles, 'base', Profile(name='base', context={'greeting': 'hi'}))
        monkeypatch.setitem(folker.profiles, 'override',
                            Profile(name='override', context={'greeting': 'hello'}))

        success, failures = ParallelExecutor().execute(
            Configuration(profiles=['base', 'override']),
            [FolkerTest(name='test', stages=[ExpectGreetingStage(name='stage', expected='hello')])])

        assert (success, failures) == (['test'], [])

    def test_variables_from_configuration_reach_the_workers(self, start_method):
        config = Configuration(context={'greeting': 'hello'})

        success, failures = ParallelExecutor().execute(config, _tests())

        assert (success, failures) == (['test_0', 'test_1'], [])

    def test_missing_variable_is_reported_as_failure(self, start_method):
        success, failures = ParallelExecutor().execute(Configuration(), _tests())

        assert (success, failures) == ([], ['test_0', 'test_1'])


def a_test(name, *stages, **fields):
    return FolkerTest(name=name, stages=list(stages) or [PassStage(name='stage')], **fields)


@pytest.mark.parametrize('start_method', START_METHODS, indirect=True)
class TestParallelExecutorResults:
    def test_no_tests(self, start_method):
        assert ParallelExecutor().execute(Configuration(), []) == ([], [])

    def test_results_follow_the_order_of_the_tests_not_the_order_they_finish(self, start_method):
        # The first test finishes last, so completion order and input order differ
        tests = [a_test('slow', SleepStage(name='s', seconds=1)),
                 a_test('fast_1'),
                 a_test('slow_failing', SleepStage(name='s', seconds=0.5), FailStage(name='f')),
                 a_test('fast_failing', FailStage(name='f')),
                 a_test('fast_2')]

        success, failures = ParallelExecutor().execute(Configuration(), tests)

        assert success == ['slow', 'fast_1', 'fast_2']
        assert failures == ['slow_failing', 'fast_failing']

    def test_a_failing_test_does_not_affect_the_others(self, start_method):
        tests = [a_test('failing', FailStage(name='f'))] + [a_test(f'ok_{i}') for i in range(3)]

        assert ParallelExecutor().execute(Configuration(), tests) == (['ok_0', 'ok_1', 'ok_2'],
                                                                      ['failing'])

    def test_more_tests_than_workers(self, start_method, monkeypatch):
        monkeypatch.setattr('folker.executor.parallel_executor.cpu_count', lambda: 2)
        tests = [a_test(f'test_{i}') for i in range(8)]

        success, failures = ParallelExecutor().execute(Configuration(), tests)

        assert success == [f'test_{i}' for i in range(8)]
        assert failures == []


@pytest.mark.parametrize('start_method', START_METHODS, indirect=True)
class TestParallelExecutorForeach:
    def test_a_test_with_foreach_is_reported_once_when_every_iteration_passes(self, start_method):
        test = a_test('loop', FailOnValueStage(name='s', variable='item', value='never'),
                      foreach={'item': ['a', 'b', 'c']})

        assert ParallelExecutor().execute(Configuration(), [test]) == (['loop'], [])

    def test_a_test_with_foreach_fails_when_one_iteration_fails(self, start_method):
        test = a_test('loop', FailOnValueStage(name='s', variable='item', value='b'),
                      foreach={'item': ['a', 'b', 'c']})

        assert ParallelExecutor().execute(Configuration(), [test]) == ([], ['loop'])

import multiprocessing

import pytest

import folker
from folker.executor import ParallelExecutor
from folker.model import Profile, Stage
from folker.model import Test as FolkerTest  # not `Test`: pytest would try to collect it
from folker.parameters import Configuration

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

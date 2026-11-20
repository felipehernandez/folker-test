import pytest

import folker
from folker.executor import SequentialExecutor
from folker.logger import LoggerType
from folker.model import Profile
from folker.model import Test as FolkerTest  # not `Test`: pytest would try to collect it
from folker.model.error import InvalidProfileSelectionException
from folker.parameters import Configuration
from tests.executor.stages import (AbsentVariableStage, CrashStage, ExpectVariableStage,
                                   FailOnValueStage, FailStage, PassStage, SaveStage)


def a_test(name, *stages, **fields):
    return FolkerTest(name=name, stages=list(stages) or [PassStage(name='stage')], **fields)


def execute(tests, config=None):
    return SequentialExecutor().execute(config or Configuration(), tests)


@pytest.fixture
def registered_profiles(monkeypatch):
    monkeypatch.setattr(folker, 'profiles', {})
    monkeypatch.setattr('folker.executor.profiles', folker.profiles)
    return folker.profiles


class TestSequentialExecutorResults:
    def test_no_tests(self):
        assert execute([]) == ([], [])

    def test_all_pass(self):
        assert execute([a_test('a'), a_test('b')]) == (['a', 'b'], [])

    def test_all_fail(self):
        tests = [a_test('a', FailStage(name='s')), a_test('b', FailStage(name='s'))]

        assert execute(tests) == ([], ['a', 'b'])

    def test_results_are_split_keeping_the_order_of_the_tests(self):
        tests = [a_test('a'), a_test('b', FailStage(name='s')), a_test('c'),
                 a_test('d', FailStage(name='s'))]

        assert execute(tests) == (['a', 'c'], ['b', 'd'])

    def test_a_failing_test_does_not_stop_the_following_ones(self):
        tests = [a_test('first', FailStage(name='s')), a_test('second')]

        assert execute(tests) == (['second'], ['first'])

    def test_a_stage_crashing_with_any_exception_fails_only_its_test(self):
        tests = [a_test('crash', CrashStage(name='s')), a_test('after')]

        assert execute(tests) == (['after'], ['crash'])


class TestSequentialExecutorIsolation:
    def test_variables_saved_by_a_test_do_not_reach_the_next_one(self):
        tests = [a_test('saves', SaveStage(name='s', variable='leak', value='x')),
                 a_test('checks', AbsentVariableStage(name='s', variable='leak'))]

        assert execute(tests) == (['saves', 'checks'], [])

    def test_every_test_gets_the_configured_variables(self):
        config = Configuration(context={'greeting': 'hello'})
        tests = [a_test(f'test_{i}', ExpectVariableStage(name='s', variable='greeting',
                                                         expected='hello'))
                 for i in range(3)]

        assert execute(tests, config) == (['test_0', 'test_1', 'test_2'], [])

    def test_a_test_changing_a_configured_variable_does_not_change_it_for_the_next(self):
        config = Configuration(context={'greeting': 'hello'})
        tests = [a_test('changes', SaveStage(name='s', variable='greeting', value='bye')),
                 a_test('checks', ExpectVariableStage(name='s', variable='greeting',
                                                      expected='hello'))]

        assert execute(tests, config) == (['changes', 'checks'], [])


class TestSequentialExecutorProfiles:
    def test_the_selected_profile_provides_context_and_secrets(self, registered_profiles):
        registered_profiles['dev'] = Profile(name='dev', context={'greeting': 'hello'},
                                             secrets={'token': 'secret'})
        tests = [a_test('t', ExpectVariableStage(name='s', variable='greeting', expected='hello'),
                        ExpectVariableStage(name='s', variable='token', expected='secret'))]

        assert execute(tests, Configuration(profiles=['dev'])) == (['t'], [])

    def test_command_line_values_win_over_the_profile(self, registered_profiles):
        registered_profiles['dev'] = Profile(name='dev', context={'greeting': 'profile'},
                                             secrets={'token': 'profile'})
        config = Configuration(profiles=['dev'], context={'greeting': 'cli'},
                               secrets={'token': 'cli'})
        tests = [a_test('t', ExpectVariableStage(name='s', variable='greeting', expected='cli'),
                        ExpectVariableStage(name='s', variable='token', expected='cli'))]

        assert execute(tests, config) == (['t'], [])

    def test_several_profiles_are_merged_with_the_last_one_winning(self, registered_profiles):
        registered_profiles['base'] = Profile(name='base', context={'a': 'base', 'b': 'base'})
        registered_profiles['override'] = Profile(name='override', context={'b': 'override'})
        tests = [a_test('t', ExpectVariableStage(name='s', variable='a', expected='base'),
                        ExpectVariableStage(name='s', variable='b', expected='override'))]

        assert execute(tests, Configuration(profiles=['base', 'override'])) == (['t'], [])

    def test_an_unknown_profile_fails_before_any_test_runs(self, registered_profiles):
        tests = [a_test('t', SaveStage(name='s', variable='ran', value=True))]

        with pytest.raises(InvalidProfileSelectionException):
            execute(tests, Configuration(profiles=['unknown']))


class TestSequentialExecutorForeach:
    def test_a_test_with_foreach_is_reported_once_when_every_iteration_passes(self):
        test = a_test('loop', FailOnValueStage(name='s', variable='item', value='never'),
                      foreach={'item': ['a', 'b', 'c']})

        assert execute([test]) == (['loop'], [])

    def test_a_test_with_foreach_fails_when_one_iteration_fails(self):
        test = a_test('loop', FailOnValueStage(name='s', variable='item', value='b'),
                      foreach={'item': ['a', 'b', 'c']})

        assert execute([test]) == ([], ['loop'])

    def test_the_following_test_runs_after_a_failing_foreach(self):
        tests = [a_test('loop', FailOnValueStage(name='s', variable='item', value='a'),
                        foreach={'item': ['a', 'b']}),
                 a_test('after')]

        assert execute(tests) == (['after'], ['loop'])


class TestSequentialExecutorLogging:
    def test_every_test_gets_its_own_sequential_logger(self, monkeypatch):
        built = []
        original = folker.executor.sequential_executor.logger_factory.build_test_logger

        def spy(config, logger_type):
            logger = original(config, logger_type)
            built.append((logger, logger_type))
            return logger

        monkeypatch.setattr(folker.executor.sequential_executor.logger_factory,
                            'build_test_logger', spy)

        execute([a_test('a'), a_test('b'), a_test('c')])

        assert [logger_type for _, logger_type in built] == [LoggerType.SEQUENTIAL] * 3
        assert len({id(logger) for logger, _ in built}) == 3

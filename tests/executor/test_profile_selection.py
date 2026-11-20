import pytest

import folker
from folker.executor import DEFAULT_PROFILE, SequentialExecutor, select_profile
from folker.model import Profile
from folker.model.error import InvalidProfileSelectionException
from folker.parameters import Configuration


@pytest.fixture
def registered_profiles(monkeypatch):
    monkeypatch.setattr(folker, 'profiles', {})
    monkeypatch.setattr('folker.executor.profiles', folker.profiles)
    for name in ('base', 'staging'):
        folker.profiles[name] = Profile(name=name, context={'env': name})
    return folker.profiles


class TestProfileSelection:
    def test_no_profile_selects_the_default(self, registered_profiles):
        assert select_profile(Configuration()) is DEFAULT_PROFILE

    def test_one_known_profile(self, registered_profiles):
        assert select_profile(Configuration(profiles={'staging'})).name == 'staging'

    def test_the_selected_profile_is_returned_as_registered(self, registered_profiles):
        assert select_profile(Configuration(profiles=['staging'])) is registered_profiles['staging']

    def test_several_profiles_are_merged(self, registered_profiles):
        registered_profiles['base'] = Profile(name='base',
                                              context={'env': 'base', 'region': 'eu'},
                                              secrets={'token': 'base-token'})
        registered_profiles['staging'] = Profile(name='staging',
                                                 context={'env': 'staging', 'debug': 'on'},
                                                 secrets={'password': 'staging-password'})

        profile = select_profile(Configuration(profiles=['base', 'staging']))

        assert profile.name == 'base,staging'
        assert profile.context == {'env': 'staging', 'region': 'eu', 'debug': 'on'}
        assert profile.secrets == {'token': 'base-token', 'password': 'staging-password'}

    def test_the_last_profile_wins_on_conflicts(self, registered_profiles):
        assert select_profile(Configuration(profiles=['base', 'staging'])).context['env'] == 'staging'
        assert select_profile(Configuration(profiles=['staging', 'base'])).context['env'] == 'base'

    def test_secrets_conflicts_follow_the_same_order(self, registered_profiles):
        registered_profiles['base'] = Profile(name='base', secrets={'token': 'one'})
        registered_profiles['staging'] = Profile(name='staging', secrets={'token': 'two'})

        assert select_profile(Configuration(profiles=['base', 'staging'])).secrets == {'token': 'two'}

    def test_nested_values_are_merged_key_by_key(self, registered_profiles):
        registered_profiles['base'] = Profile(name='base', context={
            'db': {'host': 'base-host', 'port': 5432, 'options': ['a']}})
        registered_profiles['staging'] = Profile(name='staging', context={
            'db': {'host': 'staging-host', 'options': ['b']}})

        context = select_profile(Configuration(profiles=['base', 'staging'])).context

        assert context == {'db': {'host': 'staging-host', 'port': 5432, 'options': ['b']}}

    def test_a_later_scalar_replaces_an_earlier_mapping_and_vice_versa(self, registered_profiles):
        registered_profiles['base'] = Profile(name='base', context={'a': {'x': 1}, 'b': 'text'})
        registered_profiles['staging'] = Profile(name='staging', context={'a': 'flat', 'b': {'y': 2}})

        context = select_profile(Configuration(profiles=['base', 'staging'])).context

        assert context == {'a': 'flat', 'b': {'y': 2}}

    def test_registered_profiles_are_not_modified_by_a_merge(self, registered_profiles):
        registered_profiles['base'] = Profile(name='base', context={'db': {'host': 'base-host'}})
        registered_profiles['staging'] = Profile(name='staging', context={'db': {'host': 'staging-host'}})

        merged = select_profile(Configuration(profiles=['base', 'staging']))
        merged.context['db']['host'] = 'changed'

        assert registered_profiles['base'].context == {'db': {'host': 'base-host'}}
        assert registered_profiles['staging'].context == {'db': {'host': 'staging-host'}}

    def test_a_profile_repeated_later_takes_precedence_again(self, registered_profiles):
        profile = select_profile(Configuration(profiles=['base', 'staging', 'base']))

        assert profile.context['env'] == 'base'

    def test_an_unknown_profile_among_known_ones_is_rejected(self, registered_profiles):
        with pytest.raises(InvalidProfileSelectionException) as error:
            select_profile(Configuration(profiles=['base', 'stagin']))

        assert error.value.details['selected'] == ['stagin']
        assert error.value.details['available'] == ['base', 'staging']

    def test_unknown_profile_is_rejected_with_the_available_ones(self, registered_profiles):
        with pytest.raises(InvalidProfileSelectionException) as error:
            select_profile(Configuration(profiles={'stagin'}))

        assert error.value.details['selected'] == ['stagin']
        assert error.value.details['available'] == ['base', 'staging']

    def test_unknown_profile_when_none_is_loaded(self, registered_profiles):
        registered_profiles.clear()

        with pytest.raises(InvalidProfileSelectionException) as error:
            select_profile(Configuration(profiles={'any'}))

        assert error.value.details['available'] == []


class TestExecutorsUseTheSelection:
    def test_sequential_executor_rejects_an_unknown_profile(self, registered_profiles):
        with pytest.raises(InvalidProfileSelectionException):
            SequentialExecutor().execute(Configuration(profiles={'unknown'}), [])

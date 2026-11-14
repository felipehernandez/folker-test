"""Loader tests (TST-04): globbing, templates and enrichment, profiles and error handling.

Files live in `tmp_path` and the global registries (`folker.templates`, `folker.stage_templates`,
`folker.profiles`) are replaced by empty ones for each test. Paths with unusual characters and the
`-tf` selection are in `test_load_files.py`.
"""
import pytest

from folker.load import files
from folker.load.files import load_profile_files, load_template_files, load_test_files
from folker.logger import SystemLogger
from folker.model.error import InvalidSchemaDefinitionException
from folker.module.rest.action import RestStageAction
from folker.module.void.action import VoidStageAction
from folker.parameters import Configuration


def test_yaml(name='A test', stage='A stage'):
    return (f'name: {name}\n'
            'stages:\n'
            f'  - name: {stage}\n'
            '    action:\n'
            '      type: VOID\n')


TEMPLATE = (
    'id: user_templates\n'
    'stages:\n'
    '  - id: get_user\n'
    '    name: Get user\n'
    '    action:\n'
    '      type: REST\n'
    '      method: GET\n'
    '      host: http://template-host\n'
    '      uri: users\n'
    '      headers:\n'
    '        Accept: application/json\n'
    '  - id: other_stage\n'
    '    name: Other stage\n'
    '    action:\n'
    '      type: VOID\n'
)


@pytest.fixture
def workdir(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(files, 'templates', {})
    monkeypatch.setattr(files, 'stage_templates', {})
    monkeypatch.setattr(files, 'profiles', {})
    return tmp_path


def write(directory, name, text):
    path = directory / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    return path


@pytest.fixture
def logger(mocker):
    return mocker.Mock(spec=SystemLogger)


def load_tests(logger, **options):
    return load_test_files(Configuration(**options), logger)


class TestTestFileDiscovery:
    def test_files_are_found_in_nested_directories(self, workdir, logger):
        write(workdir, 'test_root.yaml', test_yaml('root'))
        write(workdir, 'a/b/c/test_deep.yaml', test_yaml('deep'))

        assert sorted(t.name for t in load_tests(logger)) == ['deep', 'root']

    def test_only_files_matching_the_default_pattern_are_loaded(self, workdir, logger):
        write(workdir, 'test_ok.yaml', test_yaml('ok'))
        write(workdir, 'ok_test.yaml', test_yaml('suffix'))
        write(workdir, 'test_other.yml', test_yaml('yml extension'))
        write(workdir, 'template_x.yaml', TEMPLATE)
        write(workdir, 'notes.txt', 'not yaml')

        assert [t.name for t in load_tests(logger)] == ['ok']

    def test_a_custom_pattern_replaces_the_default(self, workdir, logger):
        write(workdir, 'test_default.yaml', test_yaml('default'))
        write(workdir, 'check_one.yaml', test_yaml('custom'))

        tests = load_tests(logger, test_files_re='check*.yaml')

        assert [t.name for t in tests] == ['custom']

    def test_no_files_gives_no_tests(self, workdir, logger):
        assert load_tests(logger) == []
        logger.loading_files_completed.assert_called_once_with([])

    def test_each_loaded_file_is_reported(self, workdir, logger):
        first = write(workdir, 'test_a.yaml', test_yaml('a'))
        write(workdir, 'test_b.yaml', test_yaml('b'))

        load_tests(logger)

        assert logger.loading_file_ok.call_count == 2
        reported = logger.loading_files_completed.call_args[0][0]
        assert sorted(reported) == sorted(str(p.resolve()) for p in workdir.glob('test_*.yaml'))
        assert str(first.resolve()) in reported

    def test_only_the_working_directory_is_searched(self, workdir, logger, tmp_path_factory):
        outside = tmp_path_factory.mktemp('outside')
        write(outside, 'test_outside.yaml', test_yaml('outside'))
        write(workdir, 'test_inside.yaml', test_yaml('inside'))

        assert [t.name for t in load_tests(logger)] == ['inside']


class TestBrokenFiles:
    """Today a file that cannot be loaded is logged and skipped, and the run goes on without it:
    only `-n` notices. IMP-01 makes this fail the run, which will change these tests."""

    def test_malformed_yaml_is_logged_and_skipped(self, workdir, logger):
        write(workdir, 'test_broken.yaml', 'name: [unclosed\nstages: {')
        write(workdir, 'test_ok.yaml', test_yaml('ok'))

        tests = load_tests(logger)

        assert [t.name for t in tests] == ['ok']
        (file_name, error), _ = logger.loading_file_error.call_args
        assert file_name.name == 'test_broken.yaml'
        assert error is not None

    def test_a_definition_that_does_not_match_the_schema_is_logged_and_skipped(self, workdir, logger):
        write(workdir, 'test_wrong.yaml',
              'name: Wrong\nstages:\n  - name: s\n    action:\n      type: NO_SUCH_ACTION\n')
        write(workdir, 'test_ok.yaml', test_yaml('ok'))

        assert [t.name for t in load_tests(logger)] == ['ok']
        assert logger.loading_file_error.call_count == 1

    def test_an_empty_file_is_logged_and_skipped(self, workdir, logger):
        write(workdir, 'test_empty.yaml', '')
        write(workdir, 'test_ok.yaml', test_yaml('ok'))

        assert [t.name for t in load_tests(logger)] == ['ok']
        assert logger.loading_file_error.call_count == 1

    def test_broken_files_are_not_in_the_list_of_valid_files(self, workdir, logger):
        write(workdir, 'test_broken.yaml', 'name: [unclosed')
        ok = write(workdir, 'test_ok.yaml', test_yaml('ok'))

        load_tests(logger)

        assert logger.loading_files_completed.call_args[0][0] == [str(ok.resolve())]

    def test_a_valid_file_with_missing_mandatory_fields_aborts_the_loading(self, workdir, logger):
        # Unlike the cases above, this is raised by the validation of the loaded test, which
        # runs outside the error handling of the loader
        write(workdir, 'test_invalid.yaml',
              'name: Invalid\nstages:\n  - name: s\n    action:\n      type: REST\n')

        with pytest.raises(InvalidSchemaDefinitionException) as error:
            load_tests(logger)

        assert error.value.details['missing_fields'] == {'test[Invalid].stage[s].action.host',
                                                         'test[Invalid].stage[s].action.method'}


class TestTemplates:
    def test_templates_and_their_stages_are_registered(self, workdir, logger):
        write(workdir, 'template_users.yaml', TEMPLATE)

        templates, stage_templates = load_template_files(Configuration(), logger)

        assert list(templates) == ['user_templates']
        assert sorted(stage_templates) == ['get_user', 'other_stage']
        logger.loaded_template.assert_called_once_with('user_templates')
        assert [c[0][0] for c in logger.loaded_template_stage.call_args_list] == [
            'get_user', 'other_stage']

    def test_only_files_matching_the_template_pattern_are_loaded(self, workdir, logger):
        write(workdir, 'template_a.yaml', TEMPLATE)
        write(workdir, 'test_a.yaml', test_yaml('a'))
        write(workdir, 'users_template.yaml', TEMPLATE.replace('user_templates', 'ignored'))

        templates, _ = load_template_files(Configuration(), logger)

        assert list(templates) == ['user_templates']

    def test_templates_are_found_in_nested_directories(self, workdir, logger):
        write(workdir, 'shared/templates/template_users.yaml', TEMPLATE)

        templates, _ = load_template_files(Configuration(), logger)

        assert list(templates) == ['user_templates']

    def test_the_test_file_selection_does_not_apply_to_templates(self, workdir, logger):
        write(workdir, 'template_users.yaml', TEMPLATE)

        templates, _ = load_template_files(Configuration(test_files=['test_other.yaml']), logger)

        assert list(templates) == ['user_templates']

    def test_a_broken_template_is_logged_and_skipped(self, workdir, logger):
        write(workdir, 'template_broken.yaml', 'id: [unclosed')
        write(workdir, 'template_ok.yaml', TEMPLATE)

        templates, _ = load_template_files(Configuration(), logger)

        assert list(templates) == ['user_templates']
        assert logger.loading_file_error.call_count == 1

    def test_a_stage_id_defined_twice_keeps_the_last_one_loaded(self, workdir, logger):
        # Files are read in file-system order, so which one wins is not predictable
        write(workdir, 'template_one.yaml', TEMPLATE)
        write(workdir, 'template_two.yaml', TEMPLATE.replace('user_templates', 'second')
              .replace('Get user', 'Get user, second'))

        _, stage_templates = load_template_files(Configuration(), logger)

        assert stage_templates['get_user'].name in ('Get user', 'Get user, second')
        assert len(stage_templates) == 2


class TestStageEnrichment:
    @pytest.fixture
    def templates(self, workdir, logger):
        write(workdir, 'template_users.yaml', TEMPLATE)
        load_template_files(Configuration(), logger)

    def test_a_stage_with_only_an_id_is_the_template_stage(self, workdir, logger, templates):
        write(workdir, 'test_use.yaml',
              'name: Use\nstages:\n  - id: get_user\n')

        (test,) = load_tests(logger)

        (stage,) = test.stages
        assert stage.name == 'Get user'
        assert isinstance(stage.action, RestStageAction)
        assert stage.action.host == 'http://template-host'
        assert stage.action.uri == 'users'
        assert stage.action.headers == {'Accept': 'application/json'}

    def test_a_stage_overrides_and_extends_the_template_stage(self, workdir, logger, templates):
        write(workdir, 'test_use.yaml',
              'name: Use\n'
              'stages:\n'
              '  - id: get_user\n'
              '    name: Get the first user\n'
              '    action:\n'
              '      type: REST\n'
              '      method: GET\n'
              '      uri: users/1\n'
              '      headers:\n'
              '        X-Trace: abc\n'
              '    assert:\n'
              '      - ${status_code} == 200\n')

        (test,) = load_tests(logger)

        (stage,) = test.stages
        assert stage.name == 'Get the first user'
        assert stage.action.host == 'http://template-host'
        assert stage.action.uri == 'users/1'
        assert stage.action.headers == {'Accept': 'application/json', 'X-Trace': 'abc'}
        assert stage.assertions.assertions == ['${status_code} == 200']

    def test_stages_without_an_id_and_the_order_of_stages_are_kept(self, workdir, logger, templates):
        write(workdir, 'test_use.yaml',
              'name: Use\n'
              'stages:\n'
              '  - name: before\n'
              '    action:\n'
              '      type: VOID\n'
              '  - id: other_stage\n'
              '  - name: after\n'
              '    action:\n'
              '      type: VOID\n')

        (test,) = load_tests(logger)

        assert [stage.name for stage in test.stages] == ['before', 'Other stage', 'after']

    def test_the_same_template_stage_can_be_used_by_several_tests_without_sharing_state(
            self, workdir, logger, templates):
        write(workdir, 'test_a.yaml', 'name: A\nstages:\n  - id: get_user\n'
                                      '    action:\n      type: REST\n      method: GET\n'
                                      '      uri: a\n')
        write(workdir, 'test_b.yaml', 'name: B\nstages:\n  - id: get_user\n')

        tests = {t.name: t for t in load_tests(logger)}

        assert tests['A'].stages[0].action.uri == 'a'
        assert tests['B'].stages[0].action.uri == 'users'
        assert files.stage_templates['get_user'].action.uri == 'users'

    def test_templates_are_not_enriched_by_other_templates(self, workdir, logger):
        write(workdir, 'template_users.yaml', TEMPLATE)
        write(workdir, 'template_nested.yaml',
              'id: nested\nstages:\n  - id: nested_stage\n    name: Nested\n')

        _, stage_templates = load_template_files(Configuration(), logger)

        assert isinstance(stage_templates['nested_stage'].action, VoidStageAction)

    def test_a_stage_that_has_its_own_definition_and_a_known_id_is_still_enriched(
            self, workdir, logger, templates):
        write(workdir, 'test_use.yaml',
              'name: Use\nstages:\n  - id: other_stage\n    name: Renamed\n')

        (test,) = load_tests(logger)

        assert test.stages[0].name == 'Renamed'

    def test_an_id_without_a_template_keeps_the_stage_as_written(self, workdir, logger):
        write(workdir, 'test_own.yaml',
              'name: Own\nstages:\n  - id: not_a_template\n    name: Mine\n'
              '    action:\n      type: VOID\n')

        (test,) = load_tests(logger)

        assert test.stages[0].name == 'Mine'

    @pytest.mark.xfail(strict=True, reason='BUG-22: an id that matches no template is silently '
                                           'a no-op VOID stage, so a typo gives a green test')
    def test_a_reference_to_a_template_that_does_not_exist_is_reported(self, workdir, logger,
                                                                     templates):
        write(workdir, 'test_typo.yaml', 'name: Typo\nstages:\n  - id: get_usr\n')

        try:
            tests = load_tests(logger)
        except InvalidSchemaDefinitionException:
            return

        assert logger.loading_file_error.called or tests == []


class TestProfiles:
    def test_profiles_are_registered_by_name(self, workdir, logger):
        write(workdir, 'profile_dev.yaml',
              'name: dev\ncontext:\n  host: dev-host\nsecrets:\n  token: abc\n')

        registered = load_profile_files(Configuration(), logger)

        assert list(registered) == ['dev']
        assert registered['dev'].context == {'host': 'dev-host'}
        assert registered['dev'].secrets == {'token': 'abc'}
        logger.loaded_profile.assert_called_once_with('dev')

    def test_several_profiles_in_nested_directories(self, workdir, logger):
        write(workdir, 'profile_dev.yaml', 'name: dev\n')
        write(workdir, 'envs/profile_prod.yaml', 'name: prod\n')

        assert sorted(load_profile_files(Configuration(), logger)) == ['dev', 'prod']

    def test_only_files_matching_the_profile_pattern_are_loaded(self, workdir, logger):
        write(workdir, 'profile_dev.yaml', 'name: dev\n')
        write(workdir, 'dev_profile.yaml', 'name: ignored\n')
        write(workdir, 'test_a.yaml', test_yaml('a'))

        assert list(load_profile_files(Configuration(), logger)) == ['dev']

    def test_the_test_file_selection_does_not_apply_to_profiles(self, workdir, logger):
        write(workdir, 'profile_dev.yaml', 'name: dev\n')

        registered = load_profile_files(Configuration(test_files=['test_other.yaml']), logger)

        assert list(registered) == ['dev']

    def test_a_profile_without_context_or_secrets_is_empty(self, workdir, logger):
        write(workdir, 'profile_bare.yaml', 'name: bare\n')

        profile = load_profile_files(Configuration(), logger)['bare']

        assert profile.context == {} and profile.secrets == {}

    def test_a_broken_profile_is_logged_and_skipped(self, workdir, logger):
        write(workdir, 'profile_broken.yaml', 'name: [unclosed')
        write(workdir, 'profile_ok.yaml', 'name: ok\n')

        assert list(load_profile_files(Configuration(), logger)) == ['ok']
        assert logger.loading_file_error.call_count == 1

    def test_nested_context_values_are_kept(self, workdir, logger):
        write(workdir, 'profile_dev.yaml',
              'name: dev\ncontext:\n  db:\n    host: h\n    port: 5432\n')

        assert load_profile_files(Configuration(), logger)['dev'].context == {
            'db': {'host': 'h', 'port': 5432}}

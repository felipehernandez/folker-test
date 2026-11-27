import folker.module.void  # noqa: F401  registers the VOID action type
from folker.load.schemas import StageSchema
from folker.module.void.action import VoidStageAction


def test_a_stage_without_action_gets_a_void_action():
    stage = StageSchema().load({'name': 'a stage'})

    assert isinstance(stage.action, VoidStageAction)
    assert not stage.declares_action


def test_a_stage_with_an_explicit_void_action_declares_it():
    # BUG-22 tells the two apart: only a stage that writes no action can be a template reference
    stage = StageSchema().load({'name': 'a stage', 'action': {'type': 'VOID'}})

    assert isinstance(stage.action, VoidStageAction)
    assert stage.declares_action


def test_schema_load_id():
    schema = StageSchema()

    parsed_data = schema.pre_process_spec(in_data={'id': 42})

    assert isinstance(parsed_data['id'], str)


def test_a_stage_that_names_another_method_runs_it_on_the_template_connection():
    # BUG-21: the template is a connection preset; the stage's method picks the operation
    import folker.module.postgres  # noqa: F401  registers the POSTGRES action type
    from folker.module.postgres.action import PostgresMethod, PostgresStageInsertAction

    template = StageSchema().load({'id': 'db', 'action': {
        'type': 'POSTGRES', 'method': 'SELECT', 'host': 'db-host', 'sql': 'SELECT 1'}})
    stage = StageSchema().load({'id': 'db', 'name': 'insert', 'action': {
        'type': 'POSTGRES', 'method': 'INSERT', 'sql': 'INSERT INTO t VALUES (1)'}})

    action = (template + stage).action

    assert type(action) is PostgresStageInsertAction
    assert action.method is PostgresMethod.INSERT
    assert (action.host, action.sql) == ('db-host', 'INSERT INTO t VALUES (1)')


def test_a_stage_can_override_one_field_without_repeating_the_method():
    # BUG-24: a stage without `method` used to fail to load with KeyError('method')
    import folker.module.postgres  # noqa: F401  registers the POSTGRES action type
    from folker.module.postgres.action import PostgresStageSelectAction

    template = StageSchema().load({'id': 'db', 'action': {
        'type': 'POSTGRES', 'method': 'SELECT', 'host': 'db-host', 'sql': 'SELECT 1'}})
    stage = StageSchema().load({'id': 'db', 'name': 'count', 'action': {
        'type': 'POSTGRES', 'sql': 'SELECT count(*) FROM t'}})

    action = (template + stage).action

    assert type(action) is PostgresStageSelectAction
    assert (action.host, action.sql) == ('db-host', 'SELECT count(*) FROM t')

from folker.module.wait import WaitActionSchema
from folker.module.wait.action import WaitStageAction


def test_schema_load_time():
    schema = WaitActionSchema()

    parsed_data = schema.pre_process_spec(in_data={'time': 1})

    assert isinstance(parsed_data['time'], str)


def test_schema_load_missing_time():
    schema = WaitActionSchema()

    parsed_data = schema.pre_process_spec(in_data={})

    assert 'time' not in parsed_data


def test_action_build():
    schema = WaitActionSchema()

    action = schema.make_action(data={})

    assert isinstance(action, WaitStageAction)

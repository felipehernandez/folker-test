from folker.load.schemas import StageSchema


def test_missing_action_type_resolution():
    schema = StageSchema()

    parsed_data = schema.pre_process_spec(in_data={})

    assert 'VOID' == parsed_data['action']['type']


def test_schema_load_id():
    schema = StageSchema()

    parsed_data = schema.pre_process_spec(in_data={'id': 42})

    assert isinstance(parsed_data['id'], str)

import pytest
from yaml import load, SafeLoader

from folker.module.rest import RestActionSchema
from folker.module.rest.action import RestStageAction, RestMethod


@pytest.mark.action_rest
class TestRestActionLoadSchema:
    schema = RestActionSchema()

    def test_given_basic_get(self):
        original_yaml = '''
            type: REST
            method: GET
            host: http://a_host
            uri: a_uri
        '''
        definition = load(original_yaml, Loader=SafeLoader)

        loaded_action: RestStageAction = self.schema.load(definition)

        assert type(loaded_action) is RestStageAction

        assert loaded_action.method is RestMethod.GET
        assert loaded_action.host == 'http://a_host'
        assert loaded_action.uri == 'a_uri'

    def test_given_authorization(self):
        original_yaml = '''
            type: REST
            method: POST
            host: http://a_host
            uri: a_uri
            authorization:
                user: a_user
                password: p4$$w0rd
        '''
        definition = load(original_yaml, Loader=SafeLoader)

        loaded_action: RestStageAction = self.schema.load(definition)

        assert type(loaded_action) is RestStageAction

        assert loaded_action.authorization['user'] == 'a_user'
        assert loaded_action.authorization['password'] == 'p4$$w0rd'

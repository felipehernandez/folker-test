from folker.module.rest.action import RestStageAction


class TestRestActionBuildRequestParameters:
    def test_given_minimum(self):
        stage_action = RestStageAction(
            host='a_host'
        )

        request_params = stage_action.build_request_parameters()

        assert request_params['url'] == 'a_host'
        assert request_params['headers'] == {}
        assert request_params['params'] == {}

    def test_given_basic(self):
        stage_action = RestStageAction(
            host='a_host',
            uri='an_uri'
        )

        request_params = stage_action.build_request_parameters()

        assert request_params['url'] == 'a_host/an_uri'
        assert request_params['headers'] == {}
        assert request_params['params'] == {}

    def test_given_basic_with_header(self):
        stage_action = RestStageAction(
            host='a_host',
            uri='an_uri',
            headers={
                'a_key': 'a_value'
            }
        )

        request_params = stage_action.build_request_parameters()

        assert request_params['url'] == 'a_host/an_uri'
        assert request_params['headers'] == {'a_key': 'a_value'}
        assert request_params['params'] == {}

    def test_given_basic_with_params(self):
        stage_action = RestStageAction(
            host='a_host',
            uri='an_uri',
            params={
                'a_key': 'a_value'
            }
        )

        request_params = stage_action.build_request_parameters()

        assert request_params['url'] == 'a_host/an_uri'
        assert request_params['headers'] == {}
        assert request_params['params'] == {'a_key': 'a_value'}

    def test_given_basic_json(self):
        stage_action = RestStageAction(
            host='a_host',
            uri='an_uri',
            json="{ 'a_key': 'a_value' }"
        )

        request_params = stage_action.build_request_parameters()

        assert request_params['url'] == 'a_host/an_uri'
        assert request_params['headers'] == {'Content-Type': 'application/json'}
        assert request_params['params'] == {}
        assert request_params['json'] == "{ 'a_key': 'a_value' }"

    def test_given_basic_text(self):
        stage_action = RestStageAction(
            host='a_host',
            uri='an_uri',
            body="some text"
        )

        request_params = stage_action.build_request_parameters()

        assert request_params['url'] == 'a_host/an_uri'
        assert request_params['headers'] == {}
        assert request_params['params'] == {}
        assert request_params['data'] == "some text"

    def test_given_basic_x_www_form_urlencoded(self):
        stage_action = RestStageAction(
            host='a_host',
            uri='an_uri',
            headers={
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            data={'a_key': 'a_value'}
        )

        request_params = stage_action.build_request_parameters()

        assert request_params['url'] == 'a_host/an_uri'
        assert request_params['headers'] == {'Content-Type': 'application/x-www-form-urlencoded'}
        assert request_params['params'] == {}
        assert request_params['data'] == {'a_key': 'a_value'}

    def test_given_basic_form_data(self):
        stage_action = RestStageAction(
            host='a_host',
            uri='an_uri',
            headers={
                'Content-Type': 'multipart/form-data'
            },
            data={'a_key': 'a_value'}
        )

        request_params = stage_action.build_request_parameters()

        assert request_params['url'] == 'a_host/an_uri'
        assert request_params['headers'] == {}
        assert request_params['params'] == {}
        assert request_params['files'] == {'a_key': 'a_value'}

    def test_given_basic_form_data_with_headers(self):
        stage_action = RestStageAction(
            host='a_host',
            uri='an_uri',
            headers={
                'Content-Type': 'multipart/form-data',
                'a_key': 'a_value'
            },
            data={'a_key': 'a_value'}
        )

        request_params = stage_action.build_request_parameters()

        assert request_params['url'] == 'a_host/an_uri'
        assert request_params['headers'] == {'a_key': 'a_value'}
        assert request_params['params'] == {}
        assert request_params['files'] == {'a_key': 'a_value'}

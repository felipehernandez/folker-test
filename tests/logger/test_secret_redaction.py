import json
from unittest.mock import patch, Mock

import pytest
import requests

from folker.logger.test_logger import TestLogger
from folker.model import Context
from folker.module.rest.action import RestStageAction, RestMethod
from folker.parameters import Configuration


def logged_text(logger: TestLogger) -> str:
    return '\n'.join(str(entry.text) for entry in logger.report)


@pytest.fixture
def logger():
    # The base class keeps every entry in `report` (the console subclasses flush it)
    return TestLogger(Configuration(debug=True))


def prelude(logger, secrets):
    logger.action_prelude({}, Context(secrets=secrets))


@pytest.mark.logger
class TestSecretRedaction:
    @pytest.mark.parametrize('log', ['action_debug', 'action_error', 'action_warn'])
    def test_secret_is_masked(self, logger, log):
        prelude(logger, {'token': 's3cr3t-t0ken'})

        getattr(logger, log)('Authorization: Bearer s3cr3t-t0ken')

        text = logged_text(logger)
        assert 's3cr3t-t0ken' not in text
        assert 'Authorization: Bearer ' + '*' * len('s3cr3t-t0ken') in text

    def test_nested_secret_is_masked(self, logger):
        prelude(logger, {'db': {'passwords': ['nested-secret']}})

        logger.action_debug('connect nested-secret')

        assert 'nested-secret' not in logged_text(logger)

    def test_secret_is_masked_inside_json_dump(self, logger):
        secret = 'pa"ss\\wörd'
        prelude(logger, {'password': secret})

        logger.action_debug(json.dumps({'headers': {'x': secret}}))

        text = logged_text(logger)
        assert json.dumps(secret)[1:-1] not in text
        assert 'wörd' not in text and 'w\\u00f6rd' not in text

    def test_longest_secret_is_masked_first(self, logger):
        prelude(logger, {'short': 'abc', 'long': 'abcdef'})

        logger.action_debug('value abcdef')

        assert logged_text(logger).endswith('*' * 6)

    def test_empty_and_non_string_secrets_do_not_break_the_message(self, logger):
        prelude(logger, {'empty': '', 'none': None, 'number': 1234})

        logger.action_debug('plain message 1234')

        text = logged_text(logger)
        assert 'plain message' in text
        assert '1234' not in text

    def test_message_untouched_without_secrets(self, logger):
        prelude(logger, {})

        logger.action_debug('plain message')

        assert 'plain message' in logged_text(logger)

    def test_debug_before_any_prelude(self, logger):
        logger.action_debug('plain message')

        assert 'plain message' in logged_text(logger)

    @patch.object(requests, 'get')
    def test_rest_debug_does_not_leak_resolved_secrets(self, requests_get, logger):
        response = Mock()
        response.status_code = 200
        response.headers = {}
        response.text = 'echo s3cr3t-t0ken'
        response.json.return_value = {}
        requests_get.return_value = response

        action = RestStageAction(method='GET',
                                 host='http://localhost:8080',
                                 headers={'Authorization': 'Bearer ${token}'},
                                 authorization={'user': 'u', 'password': '${password}'})
        action.method = RestMethod.GET

        action.execute(logger=logger,
                       context=Context(secrets={'token': 's3cr3t-t0ken',
                                                'password': 'p4ssw0rd-xyz'}))

        # The request itself still carries the real values
        assert requests_get.call_args.kwargs['headers']['Authorization'] \
            == 'Bearer s3cr3t-t0ken'
        text = logged_text(logger)
        assert 'Authorization' in text
        assert 's3cr3t-t0ken' not in text
        assert 'p4ssw0rd-xyz' not in text

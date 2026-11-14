import datetime
from unittest.mock import patch, Mock

import pytest
import requests

from folker.logger.test_logger import TestLogger
from folker.model import Context
from folker.module.rest.action import RestStageAction
from folker.parameters import Configuration


def mocked_response():
    response = Mock()
    response.status_code = 200
    response.headers = {}
    response.text = 'response_text'
    response.json.return_value = {}
    return response


class NotSerialisable:
    def __str__(self):
        return 'a-handle'


@pytest.mark.action_rest
class TestRestDebugLogging:
    # YAML produces dates and bytes (`!!binary`), neither of which json.dumps accepts
    @pytest.mark.parametrize('debug', [True, False])
    @pytest.mark.parametrize('value', [datetime.date(2026, 11, 10), b'bytes', NotSerialisable()],
                             ids=['date', 'bytes', 'object'])
    @patch.object(requests, 'post')
    def test_debug_logging_does_not_change_the_request(self, requests_post, value, debug):
        requests_post.return_value = mocked_response()
        logger = TestLogger(Configuration(debug=debug))
        action = RestStageAction(method='POST', host='http://localhost:8080',
                                 data={'field': value})

        context = action.execute(logger=logger, context=Context())

        requests_post.assert_called_once()
        assert requests_post.call_args.kwargs['data'] == {'field': value}
        assert 'error' not in context.stage_variables
        assert context.stage_variables['status_code'] == 200

    @patch.object(requests, 'post')
    def test_non_serialisable_values_are_still_logged(self, requests_post):
        requests_post.return_value = mocked_response()
        logger = TestLogger(Configuration(debug=True))
        action = RestStageAction(method='POST', host='http://localhost:8080',
                                 data={'field': NotSerialisable()})

        action.execute(logger=logger, context=Context())

        assert 'a-handle' in '\n'.join(str(entry.text) for entry in logger.report)

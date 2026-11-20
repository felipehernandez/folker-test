import base64
import email
from unittest.mock import Mock, patch

import pytest
from googleapiclient import errors

from folker.logger import TestLogger
from folker.model import Context
from folker.module.gmail.action import GmailStageSendAction

ACTION = 'folker.module.gmail.action'


def send_action(**fields):
    defaults = dict(method='SEND', sender='me@example.com', recipients=['a@example.com'],
                    subject='A subject', text='A text')
    return GmailStageSendAction(**{**defaults, **fields})


def decode(service):
    """The message handed to the Gmail API, parsed back from its base64 `raw` form"""
    body = service.users.return_value.messages.return_value.send.call_args.kwargs['body']
    return email.message_from_bytes(base64.urlsafe_b64decode(body['raw']))


@pytest.fixture
def logger(mocker):
    return mocker.Mock(spec=TestLogger)


@pytest.fixture
def service():
    service = Mock()
    service.users.return_value.messages.return_value.send.return_value.execute.return_value = {
        'id': 'message-id', 'labelIds': ['SENT']}
    with patch.object(GmailStageSendAction, '_get_service', return_value=service):
        yield service


@pytest.mark.action_gmail
class TestGmailSend:
    def test_the_api_response_is_saved(self, service, logger):
        context = send_action().execute(logger=logger, context=Context())

        assert context.stage_variables['response'] == {'id': 'message-id', 'labelIds': ['SENT']}
        assert 'error' not in context.stage_variables

    def test_the_message_is_sent_as_the_authenticated_user(self, service, logger):
        send_action().execute(logger=logger, context=Context())

        send = service.users.return_value.messages.return_value.send
        assert send.call_args.kwargs['userId'] == 'me'
        send.return_value.execute.assert_called_once_with()

    def test_the_headers_of_the_message(self, service, logger):
        send_action(sender='sender@example.com',
                    recipients=['a@example.com', 'b@example.com'],
                    hidden_recipients=['c@example.com'],
                    subject='Hello').execute(logger=logger, context=Context())

        message = decode(service)
        assert message['From'] == 'sender@example.com'
        assert message['To'] == 'a@example.com, b@example.com'
        assert message['Cc'] == 'c@example.com'
        assert message['Subject'] == 'Hello'

    def test_a_text_only_message(self, service, logger):
        send_action(text='plain body').execute(logger=logger, context=Context())

        parts = decode(service).get_payload()
        assert [part.get_content_type() for part in parts] == ['text/plain']
        assert parts[0].get_payload(decode=True).decode() == 'plain body'

    def test_text_and_html_are_sent_as_alternatives_in_that_order(self, service, logger):
        send_action(text='plain body', html='<b>html body</b>') \
            .execute(logger=logger, context=Context())

        message = decode(service)
        assert message.get_content_type() == 'multipart/alternative'
        parts = message.get_payload()
        assert [part.get_content_type() for part in parts] == ['text/plain', 'text/html']
        assert parts[1].get_payload(decode=True).decode() == '<b>html body</b>'

    def test_non_ascii_content_survives(self, service, logger):
        send_action(text='ünïcödé ✓').execute(logger=logger, context=Context())

        assert decode(service).get_payload()[0].get_payload(decode=True).decode() == 'ünïcödé ✓'

    def test_variables_are_resolved(self, service, logger):
        context = Context(test_variables={'who': 'folker'}, secrets={'domain': 'example.com'})

        send_action(subject='Hi ${who}', text='Dear ${who}',
                    recipients=['${who}@${domain}']).execute(logger=logger, context=context)

        message = decode(service)
        assert message['Subject'] == 'Hi folker'
        assert message['To'] == 'folker@example.com'
        assert message.get_payload()[0].get_payload(decode=True).decode() == 'Dear folker'

    def test_an_api_error_is_saved_as_text_without_failing_the_action(self, service, logger):
        response = Mock(status=403, reason='Forbidden')
        service.users.return_value.messages.return_value.send.return_value.execute.side_effect = \
            errors.HttpError(response, b'quota exceeded')

        context = send_action().execute(logger=logger, context=Context())

        assert isinstance(context.stage_variables['error'], str)
        assert '403' in context.stage_variables['error']
        assert 'response' not in context.stage_variables

    def test_a_failure_to_get_the_service_is_saved_as_the_error(self, logger):
        failure = RuntimeError('no credentials')

        with patch.object(GmailStageSendAction, '_get_service', side_effect=failure):
            context = send_action().execute(logger=logger, context=Context())

        assert context.stage_variables['error'] is failure


@pytest.mark.action_gmail
class TestGmailCredentials:
    def test_the_default_location_is_in_the_working_directory(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)

        with patch(f'{ACTION}.file.Storage') as storage:
            credentials = send_action()._get_credentials()

        storage.assert_called_once_with(str(tmp_path) + '/credentials/gmail/gmail-credentials.json')
        assert credentials is storage.return_value.get.return_value

    def test_a_credentials_path_replaces_the_default(self):
        with patch(f'{ACTION}.file.Storage') as storage:
            send_action(credentials_path='/secrets/gmail.json')._get_credentials()

        storage.assert_called_once_with('/secrets/gmail.json')

    def test_a_double_slash_in_the_path_is_collapsed(self):
        with patch(f'{ACTION}.file.Storage') as storage:
            send_action(credentials_path='/secrets//gmail.json')._get_credentials()

        storage.assert_called_once_with('/secrets/gmail.json')

    def test_the_service_authorises_the_http_client_with_the_credentials(self):
        credentials = Mock()
        with patch(f'{ACTION}.file.Storage') as storage, \
                patch(f'{ACTION}.discovery.build') as build, \
                patch(f'{ACTION}.httplib2.Http') as http:
            storage.return_value.get.return_value = credentials

            service = send_action()._get_service()

        credentials.authorize.assert_called_once_with(http.return_value)
        build.assert_called_once_with('gmail', 'v1', http=credentials.authorize.return_value)
        assert service is build.return_value

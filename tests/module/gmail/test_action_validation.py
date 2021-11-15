import pytest

from folker.module.gmail.action import GmailStageAction, GmailMethod


@pytest.mark.action_correctness
@pytest.mark.action_gmail
class TestGmailStageActionValidation:
    def test_validate_empty(self):
        action = GmailStageAction()

        assert not action
        assert not action.validation_report
        assert 'action.method' in action.validation_report.missing_fields
        assert 'action.sender' in action.validation_report.missing_fields
        assert 'action.recipients' in action.validation_report.missing_fields
        assert 'action.subject' in action.validation_report.missing_fields

    def test_wrong_method(self):
        action = GmailStageAction(method='X',
                                  sender='a_sender__email',
                                  recipients=['a_recipient_email'],
                                  subject='a_subject')

        assert not action
        assert not action.validation_report
        assert 'action.method' in action.validation_report.wrong_fields

    def test_correct_minimum(self):
        action = GmailStageAction(method=GmailMethod.SEND.name,
                                  sender='a_sender__email',
                                  recipients=['a_recipient_email'],
                                  subject='a_subject')
        assert action
        assert action.validation_report

    def test_correct_full_text(self):
        action = GmailStageAction(method=GmailMethod.SEND.name,
                                  credentials_path='a_path',
                                  sender='a_sender__email',
                                  recipients=['a_recipient_email'],
                                  hidden_recipients=['another_recipient_email'],
                                  subject='a_subject',
                                  text='some_text')
        assert action
        assert action.validation_report

    def test_correct_full_html(self):
        action = GmailStageAction(method=GmailMethod.SEND.name,
                                  credentials_path='a_path',
                                  sender='a_sender__email',
                                  recipients=['a_recipient_email'],
                                  hidden_recipients=['another_recipient_email'],
                                  subject='a_subject',
                                  html='some_html')
        assert action
        assert action.validation_report

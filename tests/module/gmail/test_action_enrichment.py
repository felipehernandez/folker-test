import pytest

from folker.module.gmail.action import GmailStageAction, GmailMethod
from folker.module.void.action import VoidStageAction


@pytest.mark.action_gmail
class TestGmailActionEnrichment:
    def test_enrich_empty(self):
        original = GmailStageAction(method=GmailMethod.SEND.name)
        enrichment = GmailStageAction(method=GmailMethod.SEND.name,
                                      sender='a_sender__email',
                                      recipients=['a_recipient_email'],
                                      subject='a_subject')

        enriched = original + enrichment

        assert enriched.method == GmailMethod.SEND
        assert enriched.sender == 'a_sender__email'
        assert enriched.recipients == ['a_recipient_email']
        assert enriched.subject == 'a_subject'

    def test_override_sender(self):
        original = GmailStageAction(method=GmailMethod.SEND.name,
                                    sender='a_sender__email',
                                    recipients=['a_recipient_email'],
                                    subject='a_subject')
        enrichment = GmailStageAction(method=GmailMethod.SEND.name,
                                      sender='another_sender__email')

        enriched = original + enrichment

        assert enriched.method == GmailMethod.SEND
        assert enriched.sender == 'another_sender__email'
        assert enriched.recipients == ['a_recipient_email']
        assert enriched.subject == 'a_subject'

    def test_merge_recipients(self):
        original = GmailStageAction(method=GmailMethod.SEND.name,
                                    sender='a_sender__email',
                                    recipients=['a_recipient_email'],
                                    subject='a_subject')
        enrichment = GmailStageAction(method=GmailMethod.SEND.name,
                                      recipients=['another_recipient_email'])

        enriched = original + enrichment

        assert enriched.method == GmailMethod.SEND
        assert enriched.sender == 'a_sender__email'
        assert enriched.recipients == ['a_recipient_email', 'another_recipient_email']
        assert enriched.subject == 'a_subject'

    def test_enrich_void(self):
        original = GmailStageAction(method=GmailMethod.SEND.name,
                                    sender='a_sender__email',
                                    recipients=['a_recipient_email'],
                                    subject='a_subject')
        enrichment = VoidStageAction()

        enriched = original + enrichment

        assert enriched.method == GmailMethod.SEND
        assert enriched.sender == 'a_sender__email'
        assert enriched.recipients == ['a_recipient_email']
        assert enriched.subject == 'a_subject'

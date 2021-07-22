import base64
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from enum import Enum, auto

import httplib2
from apiclient import errors
from googleapiclient import discovery
from oauth2client import file

from folker.decorator import timed_action, resolvable_variables, loggable_action
from folker.logger import TestLogger
from folker.model import Context
from folker.model import StageAction
from folker.module.void.action import VoidStageAction


class GmailMethod(Enum):
    SEND = auto()


class GmailStageAction(StageAction):
    method: GmailMethod
    credentials_path: str

    sender: str
    recipients: str
    hidden_recipients: str
    subject = str
    text = str
    html = str

    def __init__(self,
                 method: str = None,
                 credentials_path: str = None,
                 sender: str = None,
                 recipients: [str] = None,
                 hidden_recipients: [str] = None,
                 subject: str = None,
                 text: str = None,
                 html: str = None,
                 **kargs) -> None:
        super().__init__()

        if method:
            try:
                self.method = GmailMethod[method]
            except Exception as ex:
                self.validation_report.wrong_fields.add('action.method')

        self.credentials_path = credentials_path
        self.sender = sender
        self.recipients = recipients if recipients else []
        self.hidden_recipients = hidden_recipients if hidden_recipients else []
        self.subject = subject
        self.text = text
        self.html = html

    def __add__(self, enrichment: 'GmailStageAction'):
        result = self.__copy__()
        if isinstance(enrichment, VoidStageAction):
            return result

        if enrichment.credentials_path:
            result.credentials_path = enrichment.credentials_path
        if enrichment.sender:
            result.sender = enrichment.sender
        result.recipients = self.recipients + enrichment.recipients
        result.hidden_recipients = self.hidden_recipients + enrichment.hidden_recipients
        if enrichment.subject:
            result.subject = enrichment.subject
        if enrichment.text:
            result.text = enrichment.text
        if enrichment.html:
            result.html = enrichment.html

        return result

    def mandatory_fields(self) -> [str]:
        return [
            'method',
            'sender',
            'recipients',
            'subject'
        ]

    @loggable_action
    @resolvable_variables
    @timed_action
    def execute(self, logger: TestLogger, context: Context) -> Context:
        try:
            service = self._get_service()
            {
                GmailMethod.SEND: self._send,
            }[self.method](service, context)
        except Exception as e:
            context.save_on_stage('error', e)

        return context

    def _get_service(self):
        credentials = self._get_credentials()
        http = credentials.authorize(httplib2.Http())
        return discovery.build('gmail', 'v1', http=http)

    def _get_credentials(self):
        credentials_path = os.getcwd() + '/credentials/gmail/gmail-credentials.json'
        if self.credentials_path:
            credentials_path = self.credentials_path
        credentials_path = credentials_path.replace('//', '/')

        store = file.Storage(credentials_path)
        credentials = store.get()
        return credentials

    def _send(self, service, context):
        message = self._build_message()
        self._send_message(service, "me", message, context)

    def _build_message(self):
        message = MIMEMultipart('alternative')
        message['From'] = self.sender
        message['To'] = ', '.join(self.recipients)
        message['Cc'] = ', '.join(self.hidden_recipients)
        message['Subject'] = self.subject
        if self.text:
            message.attach(MIMEText(self.text, 'plain'))
        if self.html:
            message.attach(MIMEText(self.html, 'html'))
        return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

    def _send_message(self, service, user_id, message, context):
        try:
            message = (service.users().messages().send(userId=user_id, body=message).execute())
            context.save_on_stage('response', message)
        except errors.HttpError as error:
            context.save_on_stage('error', str(error))

from marshmallow import Schema, fields, post_load

from folker.module.gmail.action import GmailStageAction


class GmailActionSchema(Schema):
    type = fields.String()

    method = fields.String()
    credentials_path = fields.String()
    sender = fields.String(data_key='from')
    recipients = fields.List(cls_or_instance=fields.String, data_key='to')
    hidden_recipients = fields.List(cls_or_instance=fields.String, data_key='cc')
    subject = fields.String()
    text = fields.String()
    html = fields.String()

    @post_load
    def make_action(self, data, **kwargs):
        return GmailStageAction(**data)

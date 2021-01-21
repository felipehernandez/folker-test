from folker.load.schemas import ActionSchema
from folker.module.gmail.schema import GmailActionSchema

ActionSchema.type_schemas['GMAIL'] = GmailActionSchema

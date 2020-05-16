from folker.load.schemas import ActionSchema
from folker.module.gcp.pubsub.schema import PubSubActionSchema

ActionSchema.type_schemas['PUBSUB'] = PubSubActionSchema

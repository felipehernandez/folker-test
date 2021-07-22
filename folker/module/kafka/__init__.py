from folker.load.schemas import ActionSchema
from folker.module.kafka.schema import KafkaActionSchema

ActionSchema.type_schemas['KAFKA'] = KafkaActionSchema

from copy import deepcopy
from enum import Enum, auto

from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError

from folker.decorator import loggable_action, resolvable_variables, timed_action
from folker.logger import TestLogger
from folker.model import StageAction, Context
from folker.model.error import InvalidSchemaDefinitionException
from folker.module.void.action import VoidStageAction


class KafkaMethod(Enum):
    PUBLISH = auto()
    SUBSCRIBE = auto()


class KafkaStageAction(StageAction):
    method: KafkaMethod

    host: str

    topic: str
    key: str = None
    message: str = None
    headers: dict = None
    group: str

    def __init__(self,
                 method: str = None,
                 host: str = None,
                 topic: str = None,
                 key: str = None,
                 message: str = None,
                 headers: dict = None,
                 group=None
                 ):
        super().__init__()

        if method:
            try:
                self.method = KafkaMethod[method]
            except Exception as ex:
                raise InvalidSchemaDefinitionException(wrong_fields=['action.method'])

        self.host = host
        self.topic = topic
        self.key = key
        self.message = message
        self.group = group
        self.headers = [(key, value.encode()) for key, value in headers.items()] if headers else []

    def __add__(self, enrichment: 'KafkaStageAction'):
        result = self.__copy__()
        if isinstance(enrichment, VoidStageAction):
            return result

        if enrichment.host:
            result.host = enrichment.host
        if enrichment.topic:
            result.topic = enrichment.topic
        if enrichment.key:
            result.key = enrichment.key
        if enrichment.message:
            result.message = enrichment.message
        if enrichment.group:
            result.group = enrichment.group
        result.headers = self.headers + enrichment.headers

        return result

    def __copy__(self):
        return deepcopy(self)

    def mandatory_fields(self):
        return [
            'host',
            'method',
            'topic'
        ]

    def _validate_specific(self):
        if hasattr(self, 'method') and KafkaMethod.PUBLISH is self.method:
            if (not hasattr(self, 'message') or not self.message) \
                    and (not hasattr(self, 'key') or not self.key):
                self.validation_report.missing_fields.update({'action.key', 'action.message'})

    @loggable_action
    @resolvable_variables
    @timed_action
    def execute(self, logger: TestLogger, context: Context) -> Context:
        {
            KafkaMethod.PUBLISH: self._publish,
            KafkaMethod.SUBSCRIBE: self._subscribe,
        }.get(self.method)(logger, context)

        return context

    def _publish(self, logger: TestLogger, context: Context):
        producer = KafkaProducer(bootstrap_servers=[self.host])

        future = producer.send(topic=self.topic,
                               key=self.key.encode() if self.key else None,
                               value=self.message.encode() if self.message else None,
                               headers=self.headers)
        try:
            record_metadata = future.get(timeout=10)

            context.save_on_stage('topic', record_metadata.topic)
            context.save_on_stage('partition', record_metadata.partition)
            context.save_on_stage('timestamp', record_metadata.timestamp)
            context.save_on_stage('offset', record_metadata.offset)
        except KafkaError as ex:
            context.save_on_stage('error', str(ex))

    def _subscribe(self, logger: TestLogger, context: Context):
        consumer = KafkaConsumer(self.topic,
                                 group_id=self.group,
                                 auto_offset_reset='earliest',
                                 consumer_timeout_ms=10000,
                                 bootstrap_servers=[self.host])
        messages = []
        for message in consumer:
            messages.append({
                'headers': message.headers,
                'key': message.key.decode() if self._has_value(message, 'key') else None,
                'offset': message.offset,
                'timestamp': message.timestamp,
                'topic': message.topic,
                'message': message.value.decode() if self._has_value(message, 'message') else None,
            })
        context.save_on_stage('messages', messages)

    def _has_value(self, message, attribute: str):
        return hasattr(message, attribute) and getattr(message, attribute)

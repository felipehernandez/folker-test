import json
from copy import deepcopy
from enum import Enum, auto

import pika

from folker.decorator import loggable_action, resolvable_variables, timed_action
from folker.logger import TestLogger
from folker.model import StageAction, Context
from folker.model.error import InvalidSchemaDefinitionException
from folker.module.void.action import VoidStageAction


class RabbitMQMethod(Enum):
    PUBLISH = auto()
    SUBSCRIBE = auto()
    COUNT = auto()
    CLEAR = auto()


class RabbitMQStageAction(StageAction):
    method: RabbitMQMethod

    host: str
    port: str
    vhost: str

    user: str
    password: str

    exchange: str
    message: str

    queue: str
    ack: bool

    def __init__(self,
                 method: str = None,
                 host: str = None,
                 port: str = None,
                 vhost: str = None,
                 user: str = None,
                 password: str = None,
                 exchange: str = None,
                 message=None,
                 queue: str = None,
                 ack: bool = None,
                 **kargs) -> None:
        super().__init__()

        if method:
            try:
                self.method = RabbitMQMethod[method]
            except Exception as ex:
                raise InvalidSchemaDefinitionException(wrong_fields=['action.method'])

        self.host = host
        self.port = port
        self.vhost = vhost

        self.user = user
        self.password = password

        self.exchange = exchange
        self.message = message

        self.queue = queue
        self.ack = ack

    def __copy__(self):
        return deepcopy(self)

    def __add__(self, enrichment: 'RabbitMQStageAction'):
        result = self.__copy__()
        if isinstance(enrichment, VoidStageAction):
            return result

        if enrichment.host:
            result.host = enrichment.host
        if enrichment.port:
            result.port = enrichment.port
        if enrichment.vhost:
            result.vhost = enrichment.vhost
        if enrichment.user:
            result.user = enrichment.user
        if enrichment.password:
            result.password = enrichment.password
        if enrichment.exchange:
            result.exchange = enrichment.exchange
        if enrichment.message:
            result.message = enrichment.message
        if enrichment.queue:
            result.queue = enrichment.queue
        if enrichment.ack:
            result.ack = enrichment.ack

        return result

    def mandatory_fields(self):
        return [
            'method',
            'host'
        ]

    def _validate_specific(self):
        pass

    @loggable_action
    @resolvable_variables
    @timed_action
    def execute(self, logger: TestLogger, context: Context) -> Context:
        pass

    def create_connection(self):
        connection_properties = {'host': self.host}
        if self.port:
            connection_properties['port'] = self.port
        if self.vhost:
            connection_properties['virtual_host'] = self.vhost
        if self.user and self.password:
            connection_properties['credentials'] = pika.PlainCredentials(self.user, self.password)

        return pika.BlockingConnection(pika.ConnectionParameters(**connection_properties))

    @staticmethod
    def _log_debug(logger: TestLogger, **parameters):
        logger.action_debug(json.dumps(parameters))

class RabbitMQStagePublishAction(RabbitMQStageAction):
    def __init__(self, **fields):
        super().__init__(**fields)

    def _validate_specific(self):
        if not hasattr(self, 'exchange') or not self.exchange:
            self.validation_report.missing_fields.add('action.exchange')
        if not hasattr(self, 'message') or not self.message:
            self.validation_report.missing_fields.add('action.message')

    @loggable_action
    @resolvable_variables
    @timed_action
    def execute(self, logger: TestLogger, context: Context) -> Context:
        try:
            connection = self.create_connection()

            self._log_debug(logger, exchange=self.exchange, message=str(self.message))
            channel = connection.channel()

            channel.basic_publish(exchange=self.exchange,
                                  routing_key='',
                                  body=self.message.encode())
            connection.close()
            context.save_on_stage('published', True)
        except Exception as e:
            logger.action_error(e)
            context.save_on_stage('error', str(e))

        return context

class RabbitMQStageSubscribeAction(RabbitMQStageAction):
    def __init__(self, **fields):
        super().__init__(**fields)

    def _validate_specific(self):
        if not hasattr(self, 'queue') or not self.queue:
            self.validation_report.missing_fields.add('action.queue')

    @loggable_action
    @resolvable_variables
    @timed_action
    def execute(self, logger: TestLogger, context: Context) -> Context:
        try:
            connection = self.create_connection()
            channel = connection.channel()

            method_frame, header_frame, body = channel.basic_get(queue=self.queue, auto_ack=self.ack)

            connection.close()
            message = body.decode()

            self._log_debug(logger, queue=self.queue, message=str(message))

            context.save_on_stage('queue', self.queue)
            context.save_on_stage('message', message)
            context.save_on_stage('ack-ed', self.ack)
        except Exception as e:
            logger.action_error(e)
            context.save_on_stage('error', str(e))

        return context

class RabbitMQStageCountAction(RabbitMQStageAction):
    def __init__(self, **fields):
        super().__init__(**fields)

    def _validate_specific(self):
        pass

    @loggable_action
    @resolvable_variables
    @timed_action
    def execute(self, logger: TestLogger, context: Context) -> Context:
        try:
            connection = self.create_connection()
            channel = connection.channel()

            queue = channel.queue_declare(queue=self.queue, passive=True)
            queue_len = queue.method.message_count

            context.save_on_stage('result', queue_len)
        except Exception as e:
            logger.action_error(e)
            context.save_on_stage('error', str(e))

        return context

class RabbitMQStageClearAction(RabbitMQStageAction):
    def __init__(self, **fields):
        super().__init__(**fields)

    def _validate_specific(self):
        pass

    @loggable_action
    @resolvable_variables
    @timed_action
    def execute(self, logger: TestLogger, context: Context) -> Context:
        try:
            connection = self.create_connection()
            channel = connection.channel()

            result: pika.frame.Method = channel.queue_purge(queue=self.queue)

            context.save_on_stage('result', True)
            context.save_on_stage('num_messages', result.method.message_count)
        except Exception as e:
            logger.action_error(e)
            context.save_on_stage('result', False)
            context.save_on_stage('error', str(e))
        return context

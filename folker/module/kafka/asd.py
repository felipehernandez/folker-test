#
# from kafka import KafkaProducer
# from kafka.errors import KafkaError
#
from folker.logger.console_test_logger import ConsoleTestLogger
from folker.model import Context
from folker.module.kafka.action import KafkaStageAction

# print('asd')
# producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
# print('asd2')
#
# # Asynchronous by default
# future = producer.send('topic_test', b'raw_bytes')
#
# print('asd3')
# # Block for 'synchronous' sends
# try:
#     record_metadata = future.get(timeout=10)
# except KafkaError as ex:
#     # Decide what to do if produce request failed...
#     print(ex)
#     pass
#
# # Successful result returns assigned partition and offset
# print(record_metadata.topic)
# print(record_metadata.partition)
# print(record_metadata.offset)
# print(dict(record_metadata))

action = KafkaStageAction(host='localhost:9092',
                          topic='topic_test',
                          method='PUBLISH',
                          key='123',
                          message='asd')
result = action.execute(ConsoleTestLogger(), Context.EMPTY_CONTEXT())
print(result)
#
# action = KafkaStageAction(host='localhost:9092',
#                           topic='topic_test',
#                           method='PUBLISH',
#                           key='123')
# result = action.execute(ConsoleTestLogger(), Context.EMPTY_CONTEXT())
# print(result)

action = KafkaStageAction(host='localhost:9092',
                          topic='topic_test',
                          method='SUBSCRIBE')
result = action.execute(ConsoleTestLogger(), Context.EMPTY_CONTEXT())
print(result)

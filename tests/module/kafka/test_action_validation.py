import pytest

from folker.module.kafka.action import KafkaStageAction, KafkaMethod


@pytest.mark.action_correctness
@pytest.mark.action_kafka
class TestKafkaActionValidation:
    def test_validate_publish_with_key_correct(self):
        action = KafkaStageAction(method=KafkaMethod.PUBLISH.name,
                                  host='a-host',
                                  topic='a-topic',
                                  headers={'an-attribute': 'value'},
                                  key='a-key')

        assert action
        assert action.validation_report

    def test_validate_publish_with_message_correct(self):
        action = KafkaStageAction(method=KafkaMethod.PUBLISH.name,
                                  host='a-host',
                                  topic='a-topic',
                                  headers={'an-attribute': 'value'},
                                  message='a-message')

        assert action
        assert action.validation_report

    def test_validate_publish_with_key_and_message_correct(self):
        action = KafkaStageAction(method=KafkaMethod.PUBLISH.name,
                                  host='a-host',
                                  topic='a-topic',
                                  headers={'an-attribute': 'value'},
                                  key='a-key',
                                  message='a-message')

        assert action
        assert action.validation_report

    def test_validate_correct_publish_minimum_key(self):
        action = KafkaStageAction(method=KafkaMethod.PUBLISH.name,
                                  host='a-host',
                                  topic='a-topic',
                                  key='a-key')

        assert action
        assert action.validation_report

    def test_validate_correct_publish_minimum_message(self):
        action = KafkaStageAction(method=KafkaMethod.PUBLISH.name,
                                  host='a-host',
                                  topic='a-topic',
                                  message='a-message')

        assert action
        assert action.validation_report

    def test_validate_correct_publish_minimum_key_and_message(self):
        action = KafkaStageAction(method=KafkaMethod.PUBLISH.name,
                                  host='a-host',
                                  topic='a-topic',
                                  key='a-key',
                                  message='a-message')

        assert action
        assert action.validation_report

    def test_validate_correct_subscribe(self):
        action = KafkaStageAction(method=KafkaMethod.SUBSCRIBE.name,
                                  host='a-host',
                                  topic='a-topic',
                                  group='a-group')

        assert action
        assert action.validation_report

    def test_validate_correct_subscribe_minimum(self):
        action = KafkaStageAction(method=KafkaMethod.SUBSCRIBE.name,
                                  host='a-host',
                                  topic='a-topic')

        assert action
        assert action.validation_report

    def test_validate_missing_attribute_method(self):
        action = KafkaStageAction(host='a-host',
                                  topic='a-topic')

        assert not action
        assert not action.validation_report
        assert 'action.method' in action.validation_report.missing_fields

    def test_validate_missing_attribute_host(self):
        action = KafkaStageAction(method=KafkaMethod.PUBLISH.name,
                                  topic='a-topic')

        assert not action
        assert not action.validation_report
        assert 'action.host' in action.validation_report.missing_fields

    def test_validate_missing_attribute_topic(self):
        action = KafkaStageAction(method=KafkaMethod.PUBLISH.name,
                                  host='a-host')

        assert not action
        assert not action.validation_report
        assert 'action.topic' in action.validation_report.missing_fields

    def test_validate_missing_attribute_publish_key_and_message(self):
        action = KafkaStageAction(method=KafkaMethod.PUBLISH.name,
                                  host='a-host',
                                  topic='a-topic')

        assert not action
        assert not action.validation_report
        assert 'action.key' in action.validation_report.missing_fields
        assert 'action.message' in action.validation_report.missing_fields

from folker.module.gcp.pubsub.action import PubSubStageAction, PubSubMethod


class TestPubSubActionValidation:
    def test_validate_correct_publish(self):
        action = PubSubStageAction(method=PubSubMethod.PUBLISH.name,
                                   project='a-project',
                                   topic='a-topic',
                                   attributes={'an-attribute': 'value'},
                                   message='message')

        assert action
        assert action.validation_report

    def test_validate_correct_publish_minimum(self):
        action = PubSubStageAction(method=PubSubMethod.PUBLISH.name,
                                   project='a-project',
                                   topic='a-topic',
                                   message='message')

        assert action
        assert action.validation_report

    def test_validate_correct_subscribe(self):
        action = PubSubStageAction(method=PubSubMethod.SUBSCRIBE.name,
                                   project='a-project',
                                   subscription='a-subscription',
                                   ack=True)

        assert action
        assert action.validation_report

    def test_validate_correct_subscribe(self):
        action = PubSubStageAction(method=PubSubMethod.SUBSCRIBE.name,
                                   project='a-project',
                                   subscription='a-subscription')

        assert action
        assert action.validation_report

    def test_validate_missing_attribute_method(self):
        action = PubSubStageAction(project='a-project',
                                   topic='a-topic',
                                   message='message')

        assert not action
        assert not action.validation_report
        assert 'action.method' in action.validation_report.missing_fields

    def test_validate_missing_attribute_project(self):
        action = PubSubStageAction(method=PubSubMethod.PUBLISH.name,
                                   topic='a-topic',
                                   message='message')

        assert not action
        assert not action.validation_report
        assert 'action.project' in action.validation_report.missing_fields

    def test_validate_missing_attribute_topic(self):
        action = PubSubStageAction(method=PubSubMethod.PUBLISH.name,
                                   project='a-project',
                                   message='message')

        assert not action
        assert not action.validation_report
        assert 'action.topic' in action.validation_report.missing_fields

    def test_validate_missing_attribute_message(self):
        action = PubSubStageAction(method=PubSubMethod.PUBLISH.name,
                                   project='a-project',
                                   topic='a-topic')

        assert not action
        assert not action.validation_report
        assert 'action.message' in action.validation_report.missing_fields

    def test_validate_missing_attribute_subscription(self):
        action = PubSubStageAction(method=PubSubMethod.SUBSCRIBE.name,
                                   project='a-project')

        assert not action
        assert not action.validation_report
        assert 'action.subscription' in action.validation_report.missing_fields

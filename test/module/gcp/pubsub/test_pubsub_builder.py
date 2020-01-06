from unittest import TestCase
from unittest.mock import patch

from folker.model.error.load import InvalidSchemaDefinitionException
from folker.module.gcp.pubsub.builder import PubSubStageBuilder


class TestPubSubStageBuilder(TestCase):

    @patch('folker.module.gcp.pubsub.builder.PubSubActionExecutor')
    def test_given_rest_stage_then_recognise(self, MockPubSubActionExecutor):

        builder = PubSubStageBuilder()

        stage_definition = {
            'type': 'PUBSUB'
        }

        recognises = builder.recognises(stage_definition)

        self.assertTrue(recognises)

    @patch('folker.module.gcp.pubsub.builder.PubSubActionExecutor')
    def test_given_not_pubsub_stage_then_recognise(self, MockPubSubActionExecutor):
        builder = PubSubStageBuilder()

        stage_definition = {
            'type': 'OTHER'
        }

        recognises = builder.recognises(stage_definition)

        self.assertFalse(recognises)

    @patch('folker.module.gcp.pubsub.builder.PubSubActionExecutor')
    def test_given_valid_publish_pubsub_stage_then_build(self, MockPubSubActionExecutor):
        builder = PubSubStageBuilder()

        stage_definition = {
            'name': 'pubsub_stage',
            'type': 'PUBSUB',
            'action':
                {
                    'project': 'a-project',
                    'method': 'PUBLISH',
                    'topic': 'a-topic',
                    'message': 'message'
                }
        }

        stage = builder.build_stage(stage_definition)

        self.assertIsNotNone(stage)
        self.assertIsNotNone(stage.data)
        self.assertIsNotNone(stage.executors)
        self.assertIsNotNone(stage.executors.action)
        self.assertEqual(MockPubSubActionExecutor(), stage.executors.action)
        self.assertIsNotNone(stage.executors.assertion)
        self.assertIsNotNone(stage.executors.save)
        self.assertIsNotNone(stage.executors.log)

    @patch('folker.module.gcp.pubsub.builder.PubSubActionExecutor')
    def test_given_valid_subscribe_pubsub_stage_then_build(self, MockPubSubActionExecutor):
        builder = PubSubStageBuilder()

        stage_definition = {
            'name': 'pubsub_stage',
            'type': 'PUBSUB',
            'action':
                {
                    'project': 'a-project',
                    'method': 'SUBSCRIBE',
                    'subscription': 'a-topic'
                }
        }

        stage = builder.build_stage(stage_definition)

        self.assertIsNotNone(stage)
        self.assertIsNotNone(stage.data)
        self.assertIsNotNone(stage.executors)
        self.assertIsNotNone(stage.executors.action)
        self.assertEqual(MockPubSubActionExecutor(), stage.executors.action)
        self.assertIsNotNone(stage.executors.assertion)
        self.assertIsNotNone(stage.executors.save)
        self.assertIsNotNone(stage.executors.log)

    @patch('folker.module.gcp.pubsub.builder.PubSubActionExecutor')
    def test_given_valid_pubsub_stage_with_missing_action_then_exception(self, MockPubSubActionExecutor):
        builder = PubSubStageBuilder()

        stage_definition = {
            'name': 'pubsub_stage',
            'type': 'PUBSUB'
        }

        try:
            builder.build_stage(stage_definition)
            raise AssertionError('Should not get here')
        except InvalidSchemaDefinitionException as e:
            self.assertEqual(['action'], e.details['missing_fields'])

    @patch('folker.module.gcp.pubsub.builder.PubSubActionExecutor')
    def test_given_valid_pubsub_stage_with_missing_method_in_action_then_exception(self, MockPubSubActionExecutor):
        builder = PubSubStageBuilder()

        stage_definition = {
            'name': 'pubsub_stage',
            'type': 'PUBSUB',
            'action': {
                'project': 'a-project'
            }
        }

        try:
            builder.build_stage(stage_definition)
            raise AssertionError('Should not get here')
        except InvalidSchemaDefinitionException as e:
            self.assertEqual(['action.method'], e.details['missing_fields'])

    @patch('folker.module.gcp.pubsub.builder.PubSubActionExecutor')
    def test_given_valid_pubsub_stage_with_wrong_method_in_action_then_exception(self, MockPubSubActionExecutor):
        builder = PubSubStageBuilder()

        stage_definition = {
            'name': 'pubsub_stage',
            'type': 'PUBSUB',
            'action':
                {
                    'method': 'OTHER'
                }
        }

        try:
            builder.build_stage(stage_definition)
            raise AssertionError('Should not get here')
        except InvalidSchemaDefinitionException as e:
            self.assertEqual(['action.method'], e.details['wrong_fields'])

    @patch('folker.module.gcp.pubsub.builder.PubSubActionExecutor')
    def test_given_valid_publish_pubsub_stage_with_missing_topic_in_action_then_exception(self, MockPubSubActionExecutor):
        builder = PubSubStageBuilder()

        stage_definition = {
            'name': 'pubsub_stage',
            'type': 'PUBSUB',
            'action':
                {
                    'project': 'a-project',
                    'method': 'PUBLISH',
                    'message': 'a-message'
                }
        }

        try:
            builder.build_stage(stage_definition)
            raise AssertionError('Should not get here')
        except InvalidSchemaDefinitionException as e:
            self.assertEqual(['action.topic'], e.details['missing_fields'])

    @patch('folker.module.gcp.pubsub.builder.PubSubActionExecutor')
    def test_given_valid_publish_pubsub_stage_with_missing_message_in_action_then_exception(self, MockPubSubActionExecutor):
        builder = PubSubStageBuilder()

        stage_definition = {
            'name': 'pubsub_stage',
            'type': 'PUBSUB',
            'action':
                {
                    'project': 'a-project',
                    'method': 'PUBLISH',
                    'topic': 'a-topic'
                }
        }

        try:
            builder.build_stage(stage_definition)
            raise AssertionError('Should not get here')
        except InvalidSchemaDefinitionException as e:
            self.assertEqual(['action.message'], e.details['missing_fields'])

    @patch('folker.module.gcp.pubsub.builder.PubSubActionExecutor')
    def test_given_valid_subscribe_pubsub_stage_with_missing_subscription_in_action_then_exception(self, MockPubSubActionExecutor):
        builder = PubSubStageBuilder()

        stage_definition = {
            'name': 'pubsub_stage',
            'type': 'PUBSUB',
            'action':
                {
                    'project': 'a-project',
                    'method': 'SUBSCRIBE'
                }
        }

        try:
            builder.build_stage(stage_definition)
            raise AssertionError('Should not get here')
        except InvalidSchemaDefinitionException as e:
            self.assertEqual(['action.subscription'], e.details['missing_fields'])

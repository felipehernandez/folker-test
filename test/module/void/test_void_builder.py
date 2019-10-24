from unittest import TestCase

from folker.module.void import VoidStageBuilder


class TestVoidStageBuilder(TestCase):

    def test_given_void_stage_then_recognise(self):
        builder = VoidStageBuilder()

        stage_definition = {
            'type': 'VOID'
        }

        recognises = builder.recognises(stage_definition)

        self.assertTrue(recognises)

    def test_given_not_void_stage_then_recognise(self):
        builder = VoidStageBuilder()

        stage_definition = {
            'type': 'OTHER'
        }

        recognises = builder.recognises(stage_definition)

        self.assertFalse(recognises)

    def test_given_void_stage_then_build(self):
        builder = VoidStageBuilder()

        stage_definition = {
            'id': '1',
            'name': 'void_stage',
            'type': 'VOID'
        }

        stage = builder.build(stage_definition)

        self.assertIsNotNone(stage)
        self.assertIsNotNone(stage.data)
        self.assertIsNotNone(stage.executors)
        self.assertIsNotNone(stage.executors.action)
        self.assertIsNotNone(stage.executors.assertion)
        self.assertIsNotNone(stage.executors.save)
        self.assertIsNotNone(stage.executors.log)

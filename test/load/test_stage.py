from unittest import TestCase
from unittest.mock import patch

from folker.load.stage import StageBuilder
from folker.model.entity import Stage
from folker.model.error.load import UnrecognisedSchemaException


class TestStageBuilder(TestCase):

    def test_given_no_builders_then_exception(self):
        stage_builder: StageBuilder = StageBuilder()

        try:
            stage_builder.build_stage({})
            raise AssertionError('Should not get here')
        except UnrecognisedSchemaException as e:
            self.assertEqual({}, e.details['stage_definition'])

    @patch('folker.load.stage.StageBuilder')
    def test_given_builder_when_stage_is_recognised_then_stage(self, Builder):
        stage_builder: StageBuilder = StageBuilder()

        Builder.return_value.recognises.return_value = True
        Builder.return_value.build_stage.return_value = Stage()

        stage_builder.register_builder(Builder())

        stage = stage_builder.build_stage({})

        self.assertIsNotNone(stage)

    @patch('folker.load.stage.StageBuilder')
    def test_given_builder_when_stage_is_not_recognised_then_exception(self, Builder):
        stage_builder: StageBuilder = StageBuilder()

        Builder.return_value.recognises.return_value = False

        stage_builder.register_builder(Builder())

        try:
            stage_builder.build_stage({})
            raise AssertionError('Should not get here')
        except UnrecognisedSchemaException as e:
            self.assertEqual({}, e.details['stage_definition'])

from logging import Logger
from unittest import TestCase
from unittest.mock import Mock

from folker.model.context import Context
from folker.model.stage.log import StageLog


class TestStageLog(TestCase):
    stage: StageLog
    logger: Logger

    def setUp(self):
        self.stage = StageLog()
        self.logger = Mock()

    def test_given_no_log_then_nothing(self):
        context = self.stage.execute(self.logger, Context())

        self.assertEqual({}, context.test_variables)
        self.assertEqual({}, context.stage_variables)
        self.logger.return_value.log_text.assert_not_called()

    def test_given_plain_logs_then_print(self):
        self.stage.logs = ['text']

        context = self.stage.execute(self.logger, Context())

        self.assertEqual({}, context.test_variables)
        self.assertEqual({}, context.stage_variables)
        self.logger.log_text.assert_called_with('text')

    def test_given_referenced_logs_from_stage_context_then_print(self):
        self.stage.logs = ['${reference}']

        self.stage.execute(self.logger, Context({}, {'reference': 'text'}))

        self.logger.log_text.assert_called_with('text')

    def test_given_referenced_logs_from_test_context_then_print(self):
        self.stage.logs = ['${reference}']

        self.stage.execute(self.logger, Context({'reference': 'text'}, {}))

        self.logger.log_text.assert_called_with('text')

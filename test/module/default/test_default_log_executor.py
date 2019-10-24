from unittest import TestCase
from unittest.mock import patch

from folker.model.data import StageData
from folker.module.default.log_executor import DefaultLogExecutor


class TestDefaultSaveExecutor(TestCase):

    @patch('folker.module.default.log_executor.logger')
    def test_given_no_log_then_nothing(self, logger):
        executor = DefaultLogExecutor()

        stage_data = StageData(
            id='default',
            name='stage_name'
        )

        test_context, stage_context = executor.execute(stage_data, {}, {})

        self.assertEqual({}, test_context)
        self.assertEqual({}, stage_context)
        logger.return_value.log_text.assert_not_called()

    @patch('folker.module.default.log_executor.logger')
    def test_given_plain_logs_then_print(self, logger):
        executor = DefaultLogExecutor()

        stage_data = StageData(
            id='default',
            name='stage_name',
            log=['text']
        )

        executor.execute(stage_data, {}, {})

        logger.log_text.assert_called_with('text')

    @patch('folker.module.default.log_executor.logger')
    def test_given_referenced_logs_from_stage_context_then_print(self, logger):
        executor = DefaultLogExecutor()

        stage_data = StageData(
            id='default',
            name='stage_name',
            log=['${reference}']
        )

        executor.execute(stage_data, {}, {'reference': 'text'})

        logger.log_text.assert_called_with('text')

    @patch('folker.module.default.log_executor.logger')
    def test_given_referenced_logs_from_test_context_then_print(self, logger):
        executor = DefaultLogExecutor()

        stage_data = StageData(
            id='default',
            name='stage_name',
            log=['${reference}']
        )

        executor.execute(stage_data, {'reference': 'text'}, {})

        logger.log_text.assert_called_with('text')

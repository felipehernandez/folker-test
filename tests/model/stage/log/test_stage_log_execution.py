from unittest.mock import Mock

from folker.model.context import Context
from folker.model.stage.log import StageLog


class TestStageLog:
    def test_given_no_log_then_nothing(self):
        stage = StageLog()
        logger = Mock()

        context = stage.execute(logger, Context())

        assert {} == context.test_variables
        assert {} == context.stage_variables
        logger.return_value.log_text.assert_not_called()

    def test_given_plain_logs_then_print(self):
        stage = StageLog(logs=['text'])
        logger = Mock()

        context = stage.execute(logger, Context())

        assert {} == context.test_variables
        assert {} == context.stage_variables
        logger.log_text.assert_called_with('text')

    def test_given_referenced_logs_from_stage_context_then_print(self):
        stage = StageLog(logs=['${reference}'])
        logger = Mock()

        stage.execute(logger, Context({}, {'reference': 'text'}))

        logger.log_text.assert_called_with('text')

    def test_given_referenced_logs_from_test_context_then_print(self):
        stage = StageLog(logs=['${reference}'])
        logger = Mock()

        stage.execute(logger, Context({'reference': 'text'}, {}))

        logger.log_text.assert_called_with('text')

from logging import Logger
from unittest.mock import Mock

import pytest

from folker.model.context import Context
from folker.model.stage.log import StageLog


class TestStageLog:
    stage: StageLog
    logger: Logger

    @pytest.fixture(autouse=True)
    def setup(self):
        self.stage = StageLog()
        self.logger = Mock()
        yield

    def test_given_no_log_then_nothing(self):
        context = self.stage.execute(self.logger, Context())

        assert {} == context.test_variables
        assert {} == context.stage_variables
        self.logger.return_value.log_text.assert_not_called()

    def test_given_plain_logs_then_print(self):
        self.stage.logs = ['text']

        context = self.stage.execute(self.logger, Context())

        assert {} == context.test_variables
        assert {} == context.stage_variables
        self.logger.log_text.assert_called_with('text')

    def test_given_referenced_logs_from_stage_context_then_print(self):
        self.stage.logs = ['${reference}']

        self.stage.execute(self.logger, Context({}, {'reference': 'text'}))

        self.logger.log_text.assert_called_with('text')

    def test_given_referenced_logs_from_test_context_then_print(self):
        self.stage.logs = ['${reference}']

        self.stage.execute(self.logger, Context({'reference': 'text'}, {}))

        self.logger.log_text.assert_called_with('text')

    def test_enrich(self):
        stage = StageLog(logs=['log1'])
        template_stage = StageLog(logs=['log2'])

        stage.enrich(template_stage)

        assert stage.logs == ['log1', 'log2']

    def test_validate(self):
        stage = StageLog()

        stage.validate()

    def test_validate_empty(self):
        stage = StageLog(logs=['log1'])

        stage.validate()

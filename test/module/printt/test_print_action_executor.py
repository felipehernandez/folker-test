from unittest import TestCase
from unittest.mock import patch

from folker.module.printt.action_executor import PrintActionExecutor
from folker.module.printt.data import PrintStageData


class TestPrintActionExecutor(TestCase):

    @patch('folker.module.printt.action_executor.logger')
    def test_execution(self, logger):
        executor = PrintActionExecutor()

        stage_data = PrintStageData(id='1',
                                    name='print_stage',
                                    type='PRINT',
                                    action=
                                    {'message': 'Hello world'})

        test_context, stage_context = executor.execute(stage_data, {}, {})

        self.assertEqual({}, test_context)
        self.assertTrue('elapsed_time' in stage_context)
        logger.message.assert_called()

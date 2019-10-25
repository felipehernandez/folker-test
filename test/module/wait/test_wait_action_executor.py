from unittest import TestCase
from unittest.mock import patch

from folker.module.wait.action_executor import WaitActionExecutor
from folker.module.wait.data import WaitStageData


class TestWaitActionExecutor(TestCase):

    @patch('folker.module.wait.action_executor.logger')
    def test_execution(self, logger):
        executor = WaitActionExecutor()

        stage_data = WaitStageData(id='1',
                                   name='wait_stage',
                                   type='WAIT',
                                   action={'time': 0.5})

        test_context, stage_context = executor.execute(stage_data, {}, {})

        self.assertEqual({}, test_context)
        self.assertTrue('elapsed_time' in stage_context)
        self.assertTrue(stage_context['elapsed_time'] > 0.5)
        logger.action_completed.assert_called()

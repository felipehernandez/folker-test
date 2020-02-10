# from unittest import TestCase
#
# from folker.model.error.load import InvalidSchemaDefinitionException
# from folker.module.wait.action_executor import WaitActionExecutor
# from folker.module.wait.builder import WaitStageBuilder
#
#
# class TestWaitStageBuilder(TestCase):
#
#     def test_given_wait_stage_then_recognise(self):
#         builder = WaitStageBuilder()
#
#         stage_definition = {
#             'type': 'WAIT'
#         }
#
#         recognises = builder.recognises(stage_definition)
#
#         self.assertTrue(recognises)
#
#     def test_given_not_wait_stage_then_recognise(self):
#         builder = WaitStageBuilder()
#
#         stage_definition = {
#             'type': 'OTHER'
#         }
#
#         recognises = builder.recognises(stage_definition)
#
#         self.assertFalse(recognises)
#
#     def test_given_valid_wait_stage_then_build(self):
#         builder = WaitStageBuilder()
#
#         stage_definition = {
#             'name': 'wait_stage',
#             'type': 'WAIT',
#             'action':
#                 {'time': '3'}
#         }
#
#         stage = builder.build_stage(stage_definition)
#
#         self.assertIsNotNone(stage)
#         self.assertIsNotNone(stage.data)
#         self.assertIsNotNone(stage.executors)
#         self.assertIsNotNone(stage.executors.action)
#         self.assertEqual(WaitActionExecutor, type(stage.executors.action))
#         self.assertIsNotNone(stage.executors.assertion)
#         self.assertIsNotNone(stage.executors.save)
#         self.assertIsNotNone(stage.executors.log)
#
#     def test_given_valid_wait_stage_with_missing_action_then_exception(self):
#         builder = WaitStageBuilder()
#
#         stage_definition = {
#             'name': 'wait_stage',
#             'type': 'WAIT'
#         }
#
#         try:
#             builder.build_stage(stage_definition)
#             raise AssertionError('Should not get here')
#         except InvalidSchemaDefinitionException as e:
#             self.assertEqual(['action'], e.details['missing_fields'])
#
#     def test_given_valid_wait_stage_with_missing_message_in_action__then_exception(self):
#         builder = WaitStageBuilder()
#
#         stage_definition = {
#             'name': 'wait_stage',
#             'type': 'WAIT',
#             'action': {}
#         }
#
#         try:
#             builder.build_stage(stage_definition)
#             raise AssertionError('Should not get here')
#         except InvalidSchemaDefinitionException as e:
#             self.assertEqual(['action.time'], e.details['missing_fields'])

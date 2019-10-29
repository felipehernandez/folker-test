from folker.load.stage import StageBuilderStrategy
from folker.model.entity import Stage, StageExecutors
from folker.module.default.assert_executor import DefaultAssertExecutor
from folker.module.default.log_executor import DefaultLogExecutor
from folker.module.default.save_executor import DefaultSaveExecutor
from folker.module.printt.action_executor import PrintActionExecutor
from folker.module.printt.data import PrintStageData


class PrintStageBuilder(StageBuilderStrategy):

    def __init__(self) -> None:
        super().__init__()
        self._init_executors()

    def _init_executors(self):
        self.executors = StageExecutors(action=PrintActionExecutor(),
                                        assertion=DefaultAssertExecutor(),
                                        save=DefaultSaveExecutor(),
                                        log=DefaultLogExecutor())

    def recognises(self, args: dict) -> bool:
        return 'PRINT' == args['type']

    def build_stage(self, args: dict) -> Stage:
        return Stage(data=PrintStageData(**args),
                     executors=self.executors)

    def build_template(self, args: dict) -> Stage:
        return Stage(data=PrintStageData(**args, template=True),
                     executors=self.executors)

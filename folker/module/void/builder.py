from folker.load.stage import StageBuilderStrategy
from folker.model.entity import Stage, StageExecutors
from folker.module.default.action_executor import DefaultActionExecutor
from folker.module.default.assert_executor import DefaultAssertExecutor
from folker.module.default.log_executor import DefaultLogExecutor
from folker.module.default.save_executor import DefaultSaveExecutor
from folker.module.void.data import VoidStageData


class VoidStageBuilder(StageBuilderStrategy):
    executors: StageExecutors

    def __init__(self) -> None:
        super().__init__()
        self.executors = StageExecutors(action=DefaultActionExecutor(),
                                        assertion=DefaultAssertExecutor(),
                                        save=DefaultSaveExecutor(),
                                        log=DefaultLogExecutor())

    def recognises(self, args: dict) -> bool:
        return args['type'] == 'VOID'

    def build_stage(self, args: dict) -> Stage:
        return Stage(data=VoidStageData(**args),
                     executors=self.executors)

    def build_template(self, args: dict) -> Stage:
        return Stage(data=VoidStageData(**args, template=True),
                     executors=self.executors)

from folker.load.stage import StageBuilderStrategy
from folker.model.entity import Stage, StageExecutors
from folker.module.default.assert_executor import DefaultAssertExecutor
from folker.module.default.log_executor import DefaultLogExecutor
from folker.module.default.save_executor import DefaultSaveExecutor
from folker.module.wait.action_executor import WaitActionExecutor
from folker.module.wait.data import WaitStageData


class WaitStageBuilder(StageBuilderStrategy):

    def __init__(self) -> None:
        super().__init__()
        self._init_executors()

    def _init_executors(self):
        self.executors = StageExecutors(action=WaitActionExecutor(),
                                        assertion=DefaultAssertExecutor(),
                                        save=DefaultSaveExecutor(),
                                        log=DefaultLogExecutor())

    def recognises(self, args: dict) -> bool:
        return args['type'] == 'WAIT'

    def build(self, args: dict) -> Stage:
        return Stage(data=WaitStageData(**args),
                     executors=self.executors)

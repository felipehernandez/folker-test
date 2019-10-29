from folker.load.stage import StageBuilderStrategy
from folker.model.entity import Stage, StageExecutors
from folker.module.default.assert_executor import DefaultAssertExecutor
from folker.module.default.log_executor import DefaultLogExecutor
from folker.module.default.save_executor import DefaultSaveExecutor
from folker.module.rest.action_executor import RestActionExecutor
from folker.module.rest.data import RestStageData


class RestStageBuilder(StageBuilderStrategy):

    def __init__(self) -> None:
        super().__init__()
        self._init_executors()

    def _init_executors(self):
        self.executors = StageExecutors(action=RestActionExecutor(),
                                        assertion=DefaultAssertExecutor(),
                                        save=DefaultSaveExecutor(),
                                        log=DefaultLogExecutor())

    def recognises(self, args: dict) -> bool:
        return args['type'] == 'REST'

    def build_stage(self, args: dict) -> Stage:
        return Stage(data=RestStageData(**args),
                     executors=self.executors)

    def build_template(self, args: dict) -> Stage:
        return Stage(data=RestStageData(**args, template=True),
                     executors=self.executors)

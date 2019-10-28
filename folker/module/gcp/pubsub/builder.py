from folker.load.stage import StageBuilderStrategy
from folker.model.entity import Stage, StageExecutors
from folker.module.default.action_executor import DefaultActionExecutor
from folker.module.default.assert_executor import DefaultAssertExecutor
from folker.module.default.log_executor import DefaultLogExecutor
from folker.module.default.save_executor import DefaultSaveExecutor
from folker.module.gcp.pubsub.data import PubSubStageData


class PubSubStageBuilder(StageBuilderStrategy):

    def __init__(self) -> None:
        super().__init__()
        self._init_executors()

    def _init_executors(self):
        self.executors = StageExecutors(action=DefaultActionExecutor(),
                                        assertion=DefaultAssertExecutor(),
                                        save=DefaultSaveExecutor(),
                                        log=DefaultLogExecutor())

    def recognises(self, args: dict) -> bool:
        return args['type'] == 'REST'

    def build(self, args: dict) -> Stage:
        return Stage(data=PubSubStageData(**args),
                     executors=self.executors)

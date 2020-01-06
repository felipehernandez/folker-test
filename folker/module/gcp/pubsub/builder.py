from folker.load.stage import StageBuilderStrategy
from folker.model.entity import Stage, StageExecutors
from folker.model.task import ActionExecutor
from folker.module.default.assert_executor import DefaultAssertExecutor
from folker.module.default.log_executor import DefaultLogExecutor
from folker.module.default.save_executor import DefaultSaveExecutor
from folker.module.gcp.pubsub.action_executor import PubSubActionExecutor
from folker.module.gcp.pubsub.data import PubSubStageData


class PubSubStageBuilder(StageBuilderStrategy):

    def __init__(self, action: ActionExecutor = None) -> None:
        super().__init__()
        self._init_executors(action)

    def _init_executors(self, action: ActionExecutor = None):
        self.executors = StageExecutors(action=action if action else PubSubActionExecutor(),
                                        assertion=DefaultAssertExecutor(),
                                        save=DefaultSaveExecutor(),
                                        log=DefaultLogExecutor())

    def recognises(self, args: dict) -> bool:
        return 'PUBSUB' == args['type']

    def build_stage(self, args: dict) -> Stage:
        return Stage(data=PubSubStageData(**args),
                     executors=self.executors)

    def build_template(self, args: dict) -> Stage:
        return Stage(data=PubSubStageData(**args, template=True),
                     executors=self.executors)

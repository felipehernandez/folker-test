from abc import ABC

from folker.model.entity import Stage
from folker.model.error.load import UnrecognisedSchemaException


class StageBuilderStrategy(ABC):
    def recognises(self, args: dict) -> bool:
        pass

    def build(self, args: dict) -> Stage:
        pass


class StageBuilder:
    stage_strategies: [StageBuilderStrategy]

    def __init__(self) -> None:
        super().__init__()
        self.stage_strategies = []

    def register_builder(self, builder: StageBuilderStrategy):
        self.stage_strategies.append(builder)

    def build(self, args: dict) -> Stage:
        for builder in self.stage_strategies:
            if builder.recognises(args):
                return builder.build(args)

        raise UnrecognisedSchemaException(args)

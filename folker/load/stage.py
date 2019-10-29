from abc import ABC

from folker import stage_templates
from folker.model.entity import Stage
from folker.model.error.load import UnrecognisedSchemaException, SchemaReferenceNotFoundException


class StageBuilderStrategy(ABC):
    def recognises(self, args: dict) -> bool:
        pass

    def build_stage(self, args: dict) -> Stage:
        pass

    def build_template(self, args: dict) -> Stage:
        pass

    def recognises_template(self, stage: Stage) -> bool:
        pass

    def build_from_template(self, stage: Stage, args: dict) -> Stage:
        pass


class StageBuilder:
    stage_strategies: [StageBuilderStrategy]

    def __init__(self) -> None:
        super().__init__()
        self.stage_strategies = []

    def register_builder(self, builder: StageBuilderStrategy):
        self.stage_strategies.append(builder)

    def build_stage(self, data: dict, template: bool = False) -> Stage:
        if template:
            return self._build_template(data)
        elif 'id' in data:
            return self._build_from_template(data)
        else:
            return self._build_stage(data)

    def _build_template(self, data: dict) -> Stage:
        for builder in self.stage_strategies:
            if builder.recognises(data):
                return builder.build_template(data)

        raise UnrecognisedSchemaException(data)

    def _build_from_template(self, data: dict) -> Stage:
        reference_id = data['id']
        if reference_id not in stage_templates:
            raise SchemaReferenceNotFoundException(reference_id)

        stage_template = stage_templates[reference_id]
        return stage_template.enrich(data)

    def _build_stage(self, data: dict) -> Stage:
        for builder in self.stage_strategies:
            if builder.recognises(data):
                return builder.build_stage(data)

        raise UnrecognisedSchemaException(data)

from folker.model.data import StageData


class VoidStageData(StageData):

    def __init__(self, id, name, description=None, type=str, **kargs) -> None:
        super().__init__(id, name, description, type, **kargs)

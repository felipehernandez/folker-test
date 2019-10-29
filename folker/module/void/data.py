from copy import deepcopy

from folker.model.data import StageData


class VoidStageData(StageData):

    def __init__(self, name: str, description: str = None, type: str = None, id: str = None, **kargs) -> None:
        super().__init__(id, name, description, type, **kargs)

    def __copy__(self):
        return deepcopy(self)

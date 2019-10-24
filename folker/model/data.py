class ActionData:
    pass


class LogData:
    logs: [str]

    def __init__(self, logs: [str] = []) -> None:
        super().__init__()
        self.logs = logs if logs else []


class SaveData:
    save: dict

    def __init__(self, save: dict = {}) -> None:
        super().__init__()
        self.save = save if save else {}


class AssertData:
    assertions: [str]

    def __init__(self, assertions: [str] = []) -> None:
        super().__init__()
        self.assertions = assertions


class StageData:
    id: str
    name: str
    description: str
    type: str

    action: ActionData
    save: SaveData
    assertions: AssertData
    log: LogData

    def __init__(self,
                 id,
                 name,
                 description=None,
                 type: str = None,
                 **kargs) -> None:
        super().__init__()
        self.id = id
        self.name = name
        self.description = description
        self.type = type

        self.assertions = AssertData()
        self.save = SaveData(kargs['save']) if 'save' in kargs.keys() else SaveData()
        self.assertions = AssertData(kargs['assertions']) if 'assertions' in kargs.keys() else AssertData()
        self.log = LogData(kargs['log']) if 'log' in kargs.keys() else LogData()

    def __str__(self):
        return '{} - {}'.format(self.id, self.name)

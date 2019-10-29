from copy import copy, deepcopy


class ActionData:
    pass


class LogData:
    logs: [str]

    def __init__(self, logs: [str] = []) -> None:
        super().__init__()
        self.logs = logs if logs else []

    def enrich(self, logs: [str] = []):
        new_data = LogData()
        new_data.logs = []
        new_data.logs.extend(self.logs + logs)
        return new_data


class SaveData:
    save: dict

    def __init__(self, save: dict = {}) -> None:
        super().__init__()
        self.save = save if save else {}

    def enrich(self, save: dict = {}):
        new_data = SaveData()
        new_data.save = {}
        new_data.save = {**(self.save), **save}
        return new_data

    def __copy__(self):
        return copy(self)


class AssertData:
    assertions: [str]

    def __init__(self, assertions: [str] = []) -> None:
        super().__init__()
        self.assertions = assertions

    def enrich(self, assertions: [str] = []):
        new_data = AssertData()
        new_data.assertions = []
        new_data.assertions.extend(self.assertions + assertions)
        return new_data

    def __copy__(self):
        return copy(self)


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
                 id: str,
                 name: str,
                 description: str = None,
                 type: str = None,
                 **kargs) -> None:
        super().__init__()
        self.id = id
        self.name = name
        self.description = description
        self.type = type

        self.save = SaveData(kargs['save']) if 'save' in kargs.keys() else SaveData()
        self.assertions = AssertData(kargs['assertions']) if 'assertions' in kargs.keys() else AssertData()
        self.log = LogData(kargs['log']) if 'log' in kargs.keys() else LogData()

    def __str__(self):
        return '{}'.format(self.name)

    def __copy__(self):
        return deepcopy(self)

    def enrich(self, args):
        new_stage_data = self.__copy__()

        if 'action' in args:
            new_stage_data.action = new_stage_data.action.enrich(**args['action'])
        if 'save' in args:
            new_stage_data.save = new_stage_data.save.enrich(args['save'])
        if 'assertions' in args:
            new_stage_data.assertions = new_stage_data.assertions.enrich(args['assertions'])
        if 'log' in args:
            new_stage_data.log = new_stage_data.log.enrich(args['log'])

        return new_stage_data

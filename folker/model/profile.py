class Profile(dict):
    name: str
    context: dict
    secrets: dict

    def __init__(self,
                 name: str = None,
                 context: dict = None,
                 secrets: dict = None,
                 **kwargs) -> None:
        super().__init__()
        self.name = name
        self.context = context
        self.secrets = secrets

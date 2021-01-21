class Profile:
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
        self.context = context if context else {}
        self.secrets = secrets if secrets else {}

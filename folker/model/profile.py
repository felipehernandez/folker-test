class Profile:
    name: str
    context: dict

    def __init__(self,
                 name: str = None,
                 context: dict = None,
                 **kwargs) -> None:
        super().__init__()
        self.name = name
        self.context = context

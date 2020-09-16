from copy import deepcopy


def resolvable_variables(func):
    def wrapper(self, *args, **kargs):
        original_items = deepcopy(self.__dict__)
        for attribute, value in self.__dict__.items():
            if attribute in ['action', 'save', 'log']:
                continue
            new_value = kargs['context'].replace_variables(value)
            setattr(self, attribute, new_value)

        context = func(self, *args, **kargs)

        self.__dict__ = original_items

        return context

    return wrapper

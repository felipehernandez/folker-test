import time
from copy import deepcopy

from folker.util.variable import recursive_replace_variables


def timed_action(func):
    def wrapper(self, *args, **kargs):
        start = time.time()

        test_context, stage_context = func(self, *args, **kargs)

        end = time.time()
        stage_context['elapsed_time'] = int((end - start) * 1000)

        return test_context, stage_context

    return wrapper


def resolvable_variables(func):
    def wrapper(self, *args, **kargs):
        original_items = deepcopy(self.__dict__)
        for attribute, value in self.__dict__.items():
            new_value = recursive_replace_variables(kargs['test_context'], kargs['stage_context'], value)
            setattr(self, attribute, new_value)

        test_context, stage_context = func(self, *args, **kargs)

        self.__dict__ = original_items

        return test_context, stage_context

    return wrapper

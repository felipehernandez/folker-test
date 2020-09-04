import time
from copy import deepcopy

from folker import is_trace
from folker.logger.logger import TestLogger


def timed_action(func):
    def wrapper(self, *args, **kargs):
        start = time.time()

        context = func(self, *args, **kargs)

        end = time.time()
        context.save_on_stage('elapsed_time', int((end - start) * 1000))

        return context

    return wrapper


def resolvable_variables(func):
    def wrapper(self, *args, **kargs):
        original_items = deepcopy(self.__dict__)
        for attribute, value in self.__dict__.items():
            new_value = kargs['context'].replace_variables(value)
            setattr(self, attribute, new_value)

        context = func(self, *args, **kargs)

        self.__dict__ = original_items

        return context

    return wrapper


def loggable(func):
    def wrapper(self, *args, **kargs):
        if is_trace():
            logger: TestLogger = kargs['logger']
            logger.action_prelude(action=self.__dict__, context=kargs['context'])

        context = func(self, *args, **kargs)

        if is_trace():
            logger: TestLogger = kargs['logger']
            logger.action_conclusion(action=self.__dict__, context=kargs['context'])

        return context

    return wrapper

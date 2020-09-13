from folker.parameters import is_trace
from folker.logger import TestLogger


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

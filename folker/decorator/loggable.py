from folker.logger import TestLogger


def loggable_action(func):
    def wrapper(self, *args, **kargs):
        logger: TestLogger = kargs['logger']
        logger.action_prelude(action=self.__dict__, context=kargs['context'])

        context = func(self, *args, **kargs)

        logger.action_conclusion(action=self.__dict__, context=context)

        return context

    return wrapper

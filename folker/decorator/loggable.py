from folker.logger import TestLogger


def loggable_action(func):
    def wrapper(self, logger: TestLogger, *args, **kargs):
        logger.action_prelude(action=self.__dict__, context=kargs['context'])

        context = func(self, logger=logger, *args, **kargs)

        logger.action_conclusion(action=self.__dict__, context=context)

        return context

    return wrapper

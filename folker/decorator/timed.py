from time import time


def timed_action(func):
    def wrapper(self, *args, **kargs):
        start = time()

        context = func(self, *args, **kargs)

        end = time()
        context.save_on_stage('elapsed_time', int((end - start) * 1000))

        return context

    return wrapper

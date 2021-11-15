import time


def timed_action(func):
    def wrapper(self, *args, **kargs):
        start = time.perf_counter()

        context = func(self, *args, **kargs)

        end = time.perf_counter()
        context.save_on_stage('elapsed_time', int((end - start) * 1000))

        return context

    return wrapper

import time
import functools
def elapse_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print('the elapse time of {} function is {}'.format(func.__qualname__, end_time - start_time))
        return result
    return wrapper
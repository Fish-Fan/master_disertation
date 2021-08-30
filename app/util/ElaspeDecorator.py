import time
import functools
def elapse_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print('elapse time : {} executing function : {}'.format(end_time - start_time, func.__qualname__))
        return result
    return wrapper
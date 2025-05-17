import time
from functools import wraps


def cache(ttl=3600):
    store = {}

    def decorator(func):
        @wraps(func)
        def wrapped(*args):
            key = (func.__name__, args)
            if key in store:
                result, timestamp = store[key]
                if time.time() - timestamp < ttl:
                    return result
            result = func(*args)
            store[key] = (result, time.time())
            return result

        return wrapped

    return decorator

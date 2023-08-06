
import time
import logging
from functools import wraps


logging.basicConfig(level=logging.INFO)
logger = logging


def consume_time(func):
    @wraps(func)
    def __wrapper(*a, **kw):
        start_time = int(time.time())
        result = func(*a, **kw)
        if result is None:
            logger.info(f'{func.__name__} consume time {int(time.time()) - start_time}')
        else:
            logger.info(f'{func.__name__}, result: {result} consume time {int(time.time()) - start_time}')
        return result
    return __wrapper


@consume_time
def add(x, y):
    return x + y


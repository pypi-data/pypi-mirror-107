from datetime import timedelta
from functools import wraps
from typing import Callable

import arrow


def time_it(f: Callable) -> Callable:
    @wraps(f)
    def wrapper(*args, **kwargs) -> Callable:
        start_time = arrow.utcnow()
        data = f(*args, **kwargs)
        end_time = arrow.utcnow()
        delta = (end_time - start_time).microseconds
        data.timeit = str(timedelta(microseconds=delta))
        return data

    return wrapper

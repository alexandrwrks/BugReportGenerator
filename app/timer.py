import functools
import time
from typing import Callable


async def timer(func: Callable):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = await func(*args, **kwargs)
        end = time.perf_counter()
        print("Время выполнения функции: ", end - start)

        return result

    return wrapper
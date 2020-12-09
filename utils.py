from time import time
from typing import Any, Callable


def timing(func: Callable):
    def wrapper(*arg: Any, **kwargs: Any):
        tb: float = time()
        result = func(*arg, **kwargs)
        print(f'{func.__name__} takes {time() - tb}')
        return result
    return wrapper


class ValidationException(Exception):
    def __init__(self, msg: str, reason: str) -> None:
        self.reason = reason
        self.msg = msg
        super().__init__(msg)

    def __str__(self) -> str:
        return self.msg

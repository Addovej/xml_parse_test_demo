from time import time


def timing(func):
    def wrapper(*arg, **kw):
        tb = time()
        result = func(*arg, **kw)
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

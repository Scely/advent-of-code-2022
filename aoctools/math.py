from functools import reduce
from typing import Iterable


def mul(l: Iterable[bool | int], start: int = ...) -> int:
    return reduce(lambda x, y: x * y, l)

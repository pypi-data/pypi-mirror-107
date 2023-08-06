# coding=utf-8
from typing import Iterable


def lucas() -> Iterable[int]:
    yield 2  # special case
    yield 1  # special case
    prev: int = 2  # initially set to lucas(0)
    curr: int = 1  # initially set to lucas(1)
    while True:
        prev, curr = curr, prev + curr
        yield curr

# coding=utf-8
from typing import Iterable


def fibonacci() -> Iterable[int]:
    yield 0  # special case
    yield 1  # special case
    prev: int = 0  # fib(0)
    curr: int = 1  # fib(1)
    while True:
        prev, curr = curr, prev + curr
        yield curr

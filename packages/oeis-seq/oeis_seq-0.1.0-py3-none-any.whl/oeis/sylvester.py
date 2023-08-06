# coding=utf-8
from typing import Iterable


def sylvester() -> Iterable[int]:
    prev: int = 2  # sylvester(0)
    while True:
        yield prev
        prev = (prev * (prev - 1)) + 1

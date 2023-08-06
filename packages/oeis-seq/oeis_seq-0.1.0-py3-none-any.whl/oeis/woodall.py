# coding=utf-8
from typing import Iterable
from itertools import count


def woodall() -> Iterable[int]:
    for n in count(start=1):
        yield n * (2 ** n) - 1

# coding=utf-8
from typing import Iterable
from itertools import count


def factorial() -> Iterable[int]:
    curr: int = 1
    for n in count(start=1):
        yield curr
        curr *= n

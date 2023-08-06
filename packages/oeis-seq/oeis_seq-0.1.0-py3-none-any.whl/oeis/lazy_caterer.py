# coding=utf-8
from typing import Iterable
from itertools import count


def lazy_caterer() -> Iterable[int]:
    yield 1  # special case
    yield 2  # special case
    for i in count(start=2):
        yield ((i * i) + i + 2) // 2

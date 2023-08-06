# coding=utf-8
from math import comb
from itertools import count
from typing import Iterable


def catalan() -> Iterable[int]:
    yield 1  # catalan(0)
    for n in count(start=1):
        yield comb(2 * n, n) - comb(2 * n, n - 1)

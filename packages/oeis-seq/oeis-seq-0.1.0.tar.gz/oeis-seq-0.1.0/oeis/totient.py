# coding=utf-8
from typing import Iterable, List
from .utils import coprime
from itertools import count


def totient() -> Iterable[int]:
    yield 1  # totient(0)
    for n in count(start=2):
        totients: List[bool] = [coprime(n, p) for p in range(1, n)]
        yield totients.count(True)

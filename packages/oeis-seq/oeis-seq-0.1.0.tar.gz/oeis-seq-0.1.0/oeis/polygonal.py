# coding=utf-8
from typing import Iterable


def polygonal(k: int) -> Iterable[int]:
    yield 0
    prev: int = 1
    curr: int = 1
    while True:
        yield prev
        prev, curr = prev + curr + k, curr + k


def natural() -> Iterable[int]:
    return polygonal(0)


def triangular() -> Iterable[int]:
    return polygonal(1)


def square() -> Iterable[int]:
    return polygonal(2)


def pentagonal() -> Iterable[int]:
    return polygonal(3)


def hexagonal() -> Iterable[int]:
    return polygonal(4)


def heptagonal() -> Iterable[int]:
    return polygonal(5)


def octagonal() -> Iterable[int]:
    return polygonal(6)


def nonagonal() -> Iterable[int]:
    return polygonal(7)


def decagonal() -> Iterable[int]:
    return polygonal(8)


def hendecagonal() -> Iterable[int]:
    return polygonal(9)


def dodecagonal() -> Iterable[int]:
    return polygonal(10)

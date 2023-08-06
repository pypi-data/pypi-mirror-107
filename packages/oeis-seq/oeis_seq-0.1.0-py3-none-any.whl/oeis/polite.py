# coding=utf-8
from math import floor, log2
from typing import Iterable
from itertools import count


def polite() -> Iterable[int]:
    for i in count(start=2):
        yield i + floor(log2(i + log2(i)))

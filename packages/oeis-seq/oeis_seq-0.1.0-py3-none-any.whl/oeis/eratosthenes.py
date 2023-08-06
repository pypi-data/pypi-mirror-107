# coding=utf-8
from typing import Iterable


def eratosthenes() -> Iterable[int]:
    """
    Sieve of Eratosthenes
    """
    discards = {}
    p: int = 2

    while True:
        if p not in discards:
            yield p
            discards[p * p] = [p]
        else:
            for n in discards[p]:
                discards.setdefault(p + n, []).append(n)
            del discards[p]
        p += 1

# coding=utf-8

from math import gcd

__all__ = ["coprime"]


def coprime(a: int, b: int) -> bool:
    return gcd(a, b) == 1

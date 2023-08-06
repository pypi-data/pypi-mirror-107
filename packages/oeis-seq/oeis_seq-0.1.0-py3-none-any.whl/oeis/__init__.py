# coding=utf-8
from .catalan import catalan
from .centered_polygonal import centered_polygonal, centered_square, centered_triangular
from .eratosthenes import eratosthenes
from .factorial import factorial
from .fibonacci import fibonacci
from .jacobsthal import jacobsthal
from .lazy_caterer import lazy_caterer
from .leonardo import leonardo
from .lucas import lucas
from .padovan import padovan
from .pell import pell
from .perrin import perrin
from .polite import polite
from .polygonal import (
    decagonal,
    dodecagonal,
    hendecagonal,
    heptagonal,
    hexagonal,
    natural,
    nonagonal,
    octagonal,
    pentagonal,
    polygonal,
    square,
    triangular,
)
from .pyramidal import pyramidal, square_pyramidal, triangular_pyramidal
from .recaman import recaman
from .sylvester import sylvester
from .totient import totient
from .tribonacci import tribonacci
from .woodall import woodall

__version__ = "0.1.0"
__all__ = [
    "catalan",
    "centered_polygonal",
    "centered_square",
    "centered_triangular",
    "decagonal",
    "dodecagonal",
    "eratosthenes",
    "factorial",
    "fibonacci",
    "hendecagonal",
    "heptagonal",
    "hexagonal",
    "jacobsthal",
    "lazy_caterer",
    "leonardo",
    "lucas",
    "natural",
    "nonagonal",
    "octagonal",
    "padovan",
    "pell",
    "pentagonal",
    "perrin",
    "polite",
    "polygonal",
    "recaman",
    "square",
    "sylvester",
    "square_pyramidal",
    "totient",
    "triangular",
    "triangular_pyramidal",
    "tribonacci",
    "woodall",
]

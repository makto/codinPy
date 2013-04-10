#!/usr/bin/env python
"""
Discover all the fractions with an unorthodox cancelling method.
"""

from fractions import Fraction
from itertools import product
from operator import mul

result = []
for numer in range(10, 100):
    for denom in range(10, 100):
        if numer >= denom:          # The frac shoule be less than 1
            continue

        frac = Fraction(numer, denom)

        possibles = product(tuple(str(numer)), tuple(str(denom)))
        for i, j in possibles:
            m = str(numer).replace(i, '')
            n = str(denom).replace(j, '')
            if m != n:
                continue

            i, j = int(i), int(j)
            if j == 0:
                continue

            new_frac = Fraction(i, j)
            if new_frac == frac:
                if i * 10 == numer or i * 11 == numer:
                    continue
                print numer, denom, i, j
                result.append(frac)

# Yeah....Python has fraction module
print reduce(mul, result).denominator

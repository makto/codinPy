#!/usr/bin/env python
"""
Common tools.
Never give a python file numeric name!
"""

from math import sqrt

def is_prime(n):
    if type(n) is not int:
        raise TypeError
    if n < 2:
        raise ValueError
    if n % 2 == 0:
        if n == 2:
            return True
        return False

    limit = int(sqrt(n) + 1)
    for i in xrange(2, limit):
        if n % i == 0:
            return False

    return True

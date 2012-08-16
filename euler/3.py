#! /usr/bin/env python
# Find the largest prime factor of a composite number.
# 600851475143, for example

from math import sqrt

def is_prime(n):
    """not for universal judgement"""
    i = 2
    while i < sqrt(n):
        if n % i == 0:
            return False
        i += 1
    return True

def find(n):
    half = n / 2
    if half % 2 == 0:
        half -= 1
    small = 2
    i = half        # i is always odd
    while i > 1:    # numbers too large to use for loop
        if n % i == 0 and is_prime(i):
            return i
        small += 1
        i = n / small    # reduce the computing times
#TODO: small and large method
    return 'NotFound'

if __name__ == '__main__':
    n = 600851475143
    print find(n)

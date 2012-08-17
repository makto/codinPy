#!/usr/bin/env python
"""
Find the largest prime factor of a composite number.
600851475143, for example
"""

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
    small = 3
    limit = int(sqrt(n)) + 1
    result = []
    while small < limit:      # 600851475143 is too large to use forloop in Python
        if n % small == 0:    # use the small one to find factor will be more sufficient
            if is_prime(small):
                result.append(small)
            large = n / small
            if is_prime(large):
                result.append(large)
        small += 2            # because 600851475143 is odd
    return max(result)             # the factor will never be even

if __name__ == '__main__':
    n = 600851475143
    print find(n)

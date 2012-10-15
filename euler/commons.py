#!/usr/bin/env python
"""
Common tools.
Never give a python file numeric name!
"""

from math import sqrt

def is_prime(n):
    n = int(n)
    if n < 2:
        return False
        #raise ValueError
    if n % 2 == 0:
        if n == 2:
            return True
        return False

    limit = int(sqrt(n) + 1)
    for i in xrange(2, limit):
        if n % i == 0:
            return False

    return True

def divisors(num):
    "for positive numbers"
    divs = set()
    limit = int(sqrt(num) + 1)
    for i in xrange(1, limit):
        if num % i == 0:
            divs.update({i, num/i})
    return divs
  
if __name__ == '__main__':
    print "this is a module"

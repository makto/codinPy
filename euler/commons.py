#!/usr/bin/env python
"""
Common tools.
Never give a python file numeric name!
"""

from math import sqrt
import time

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        print "Time consumed: %ss" % (time.time()-start)
    return wrapper

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
  
def is_right_triangle(a, b, c):
    sides = sorted([a,b,c])
    if sides[2]**2 == sides[1]**2 + sides[0]**2:
        return True
    else:
        return False

if __name__ == '__main__':
    print "this is a module"

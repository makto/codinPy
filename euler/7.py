#!/usr/bin/env python
"""
Find the 10001st prime.
"""

from math import sqrt

def is_prime(n):
    "for universal usage."
    if type(n) is not int:
        raise TypeError
    if n < 2:
        raise ValueError

    limit = int(sqrt(n) + 1)
    for i in xrange(2, limit):
        if n % i == 0:
            return False

    return True

i = 2
counter = 1         # yep, already count 2 in
while True:
    i += 1
    if i % 2 == 0:  #this is why 2 is counted before hand
        continue
    if is_prime(i):
        counter += 1
        if counter == 10001:
            print i
            break
print 'Done'

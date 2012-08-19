#!/usr/bin/env python

"""
Find the only Pythagorean triplet, {a, b, c}, for which a + b + c = 1000.
"""

for i in xrange(1, 999):
    pow_i = i**2
    for j in xrange(1, 1000-i):
        if j > i:
            break   # save a lot of time
        k = 1000-i-j
        if pow_i + j**2 == k**2:
            print i, j, k
            print i*j*k
            exit(0)

#!/usr/bin/env python

"""
Calculate the sum of all the primes below two million.
"""

from commons import is_prime

print sum([i for i in xrange(2, 2000000) if is_prime(i)])

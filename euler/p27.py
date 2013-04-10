#!/usr/bin/env python
"""
Find a quadratic formula that produces the maximum number of primes for consecutive values of n.
"""

from commons import is_prime

def formula(a, b, n):
    return n**2 + a*n + b

maximum = [0, None, None]

for a in xrange(-999, 1000):
    for b in xrange(2, 1000):       # b can't be negative

        ### the following trick could not speed up the program significantly. ###

        # trans the formula to:  n(n+a)+b
        # solve the equotion: n = +-b, n+a = -+b
        #possible_n = sorted((-b, b, -b-a, b-a))
        #upper_limit = None
        #for p_n in possible_n:
        #    if p_n > 0:
        #        upper_limit = p_n
        #        break

        #if upper_limit != None and upper_limit <= maximum[0]:
        #    continue

        ### end of trick ###

        n = 0
        while True:
            if is_prime(formula(a,b,n)):
                n += 1
            else:
                break

        if n > maximum[0]:
            maximum = [n, a, b]     # n stands for the number of primes. It's a trick.
        print a, b, n###

print maximum

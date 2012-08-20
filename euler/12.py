#!/usr/bin/env python
"""
What is the value of the first triangle number to have over five hundred divisors?
The 3rd triangle number is 1+2+3=6
The 7th triangle number would be 1+2+3+4+5+6=28
So, that's clear.
"""

from math import sqrt

tri_num = 0
order = 1
while True:
    tri_num += order

    mid_divisor = sqrt(tri_num)

    divisors = []
    limit = int(mid_divisor+1)
    for i in xrange(1, limit):
        if tri_num % i == 0:
            divisors.append(i)

    length = len(divisors) * 2
    if mid_divisor == divisors[-1]:
        num_of_div = length - 1
    else:
        num_of_div = length

    if num_of_div >= 500:
        print tri_num
        break

    order += 1

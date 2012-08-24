#!/usr/bin/env python
"""
Evaluate the sum of all amicable pairs under 10000.
"""

from math import sqrt

def divisors(num):
    "for positive numbers"
    divs = set()
    limit = int(sqrt(num) + 1)
    for i in xrange(1, limit):
        if num % i == 0:
            divs.update({i, num/i})
    return divs

amicables = set()
for num in xrange(1, 10000):
    num_div_sum = sum(divisors(num)) - num
    sum_div_sum = sum(divisors(num_div_sum)) - num_div_sum
    if sum_div_sum == num and sum_div_sum < 10000 and num != num_div_sum:
        amicables.update({num, num_div_sum})

print sum(amicables)

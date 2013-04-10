#!/usr/bin/env python
"""
Find the sum of all eleven primes that are both truncatable from left to right and right to left.
"""

from commons import is_prime
from itertools import product

def all_prime(number):
    l_to_r = range(1, len(number)-1)
    r_to_l = range(2-len(number), 0)

    for i in l_to_r:
        if not is_prime(int(number[i:])):
            return False
    for j in r_to_l:
        if not is_prime(int(number[:j])):
            return False

    return True

mid_len = 1
middles = ['']
result = []
while True:
    for middle in middles:
        for first in ['2', '3', '5', '7']:
            for last in ['3', '7']:
                number = first + ''.join(middle) + last
                if is_prime(int(number)) and all_prime(number):
                    result.append(int(number))
    if len(result) >= 11:
        print result
        break
    middles = product(['1','3','7','9'], repeat=mid_len)
    mid_len += 1

print sum(result)


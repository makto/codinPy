#!/usr/bin/env python
"""
How many circular primes are there below one million?
"""
from commons import is_prime

def all_prime(alters):
    for alter in alters:
        if not is_prime(int(''.join(alter))):
            return False
    return True

def circles(string):
    """make circle-numbers, which may be for general use later
    e.g. 197's circle-numbers are 971, 719"""
    numbers = []
    current = string
    for i in range(len(string)-1):
        new = current[1:] + current[0]
        numbers.append(new)
        current = new
    return numbers

result = []
for number in xrange(1000000):
    if is_prime(number):
        string = str(number)
        alters = circles(string)
        if all_prime(alters):
            result.append(number)

print len(result)
print result

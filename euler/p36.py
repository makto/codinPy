#!/usr/bin/env python
"""
Find the sum of all numbers less than one million, which are palindromic in base 10 and base 2.
"""

def is_palin(string):
    if string == ''.join(reversed(string)):
        return True
    else:
        return False

result = []
for number in xrange(1000000):
    num_bin = bin(number)[2:]
    num_int = str(number)
    if is_palin(num_bin) and is_palin(num_int):
        result.append(number)

print sum(result)

#!/usr/bin/env python
"""
Find the sum of all numbers which are equal to the sum of the factorial of their digits.
"""

from math import factorial
from itertools import combinations_with_replacement

# Somewhat like 30.py
# There is also a point where the sum of
# factorials will never catch up with the number.

max_fac = factorial(9)
max_digits = 2
while True:
    max_sum = max_fac * max_digits
    min_num = 10 ** (max_digits-1)
    print max_sum, min_num
    if max_sum < min_num:
        break
    max_digits += 1
print max_digits

def could_match(number, left):
    "test whether left could make up number"
    left_str = ''.join(left)
    for digit in set(left):
        if left_str.count(digit) != number.count(digit):
            return False
    return True

result = []
for digits in range(2, max_digits):
    # How sweet Python is!
    # Love this ..._with_replacement!
    left_part = combinations_with_replacement('0123456789', digits)
    for left in left_part:
        left_int = map(int, left)
        number = sum(map(factorial, left_int))
        number_str = str(number)
        if len(number_str) != digits:
            continue
        if could_match(number_str, left):
            result.append(number)

print result

# pretty fast!

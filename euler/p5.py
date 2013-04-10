#!/usr/bin/env python
"""
What is the smallest number divisible by each of the numbers 1 to 20?
"""

from operator import mul

nums = range(1,21)

def still_valid(num):
    for i in nums:
        if num % i != 0:
            return False
    return True

def find():
    origin = reduce(mul, nums)
    while True:
        compare = origin
        for i in nums:
            if origin % (i**2) == 0:
                tmp = origin / i
                if still_valid(tmp):
                    origin = tmp
        if origin == compare:
            break
    return origin

print find()

# the result is 232792560, which is quite surprizing.

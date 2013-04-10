#!/usr/bin/env python
"""
Find the sum of digits in 100!
"""

from math import factorial
# I know..., for Python it's just so simple.

result = factorial(100)
str_of_result = str(result)

print sum([int(i) for i in str_of_result])

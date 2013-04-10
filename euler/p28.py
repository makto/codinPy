#!/usr/bin/env python
"""
What is the sum of both diagonals in a 1001 by 1001 spiral?
"""

from operator import add

init = 1
result = 1

for i in xrange(500):
    incre = 2 * (i+1)

    four = [ init+incre*i for i in (1,2,3,4) ]
    circle = sum(four)
    result += circle

    init = four[-1]

print result

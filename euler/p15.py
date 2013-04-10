#!/usr/bin/env python
"""
Starting in the top left corner in a 20 by 20 grid, how many routes are there to the bottom right corner?
"""

# assume that the top left corner is (0, 0)
# then the down right corner is (20, 20)

from math import factorial

print factorial(40) / factorial(40-20) / factorial(20)
# the result is 137846528820
# suprising.

#########
# the following method simulates the path-chosing process.
# it can handle 100,000 paths per second.
# given the total 100,000,000,000 paths, it'll take 115 days or so.
# can't imagine that!
#########

def find(x, y, num):
    if x + 1 < 21:
        if y == 20:
            return num
        num += 1
        num = find(x+1, y, num)
    if y + 1 < 21:
        if x == 20:
            return num
        num += 1
        num = find(x, y+1, num)
    print num
    return num

# num = find(0,0,0)
# print num

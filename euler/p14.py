#!/usr/bin/env python
"""
Find the longest sequence using a starting number under one million.
The sequence is defined as below:
    n => n/2 (if n is even)
    n => 3n + 1 (if n is odd)
So, if we start with 13, the sequence generated is:
    13 => 40 => 20 => 10 => 5 => 16 => 8 => 4 => 2 => 1
"""

def find_len(n):
    length = 1
    while n != 1:
        if n % 2 == 0:
            n = n / 2
        else:
            n = 3 * n + 1
        length += 1
    return length

max_len = 1
start_num = 1
for i in xrange(1, 1000001):
    length = find_len(i)
    if length > max_len:
        max_len = length
        start_num = i

print start_num, max_len

# the starting number is 837799
# the max length is 525

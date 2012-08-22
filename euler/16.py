#!/usr/bin/env python
"""
What is the sum of the digits of the number 2 ** 1000?
"""

def way_1():
    # as we know, 2**1 = 0x10, 2**2 = 0x100, ...
    # so we can get the result of 2**1000 in binary without actually calculating.
    bin_sum = '1' + ''.join(['0']*1000)
    dec_sum = str(int(bin_sum, 2))
    sum_of_digits = sum([int(i) for i in dec_sum])
    print sum_of_digits

def way_2():
    # but Python calculates in Binary internally.
    # so just use 2 ** 1000. It's even faster!
    sum_in_str = str(2 ** 1000)
    sum_of_digits = sum([int(i) for i in sum_in_str])
    print sum_of_digits

import time
t1 = time.time()
way_1()
t2 = time.time()
print t2 - t1

t3 = time.time()
way_2()
t4 = time.time()
print t4 - t3

#!/usr/bin/env python
"""
Find the value of d<1000 for which 1/d contains the longest recurring cycle.
"""

import re
import decimal

decimal.getcontext().rounding = 'ROUND_DOWN'

max_len = 0
target_denom = 2
one = decimal.Decimal(1)
for i in range(2, 1000):
    decimal.getcontext().prec = 100             # default prec
    denominator = decimal.Decimal(i)
    recur = re.compile(r'(\d+?)\1{3,}')

    while True:
        str_decimal = str(one / denominator)
        precise = decimal.getcontext().prec
        if len(str_decimal) < precise+2:        # escape the finite decimal
            print i
            break
    
        cycle = re.findall(recur, str_decimal)
        if len(cycle) != 1:                     # the prec is not enough
            decimal.getcontext().prec += 1000   # will be faster if this prec-incr is larger
            continue                            # which is interesting
        else:
            recur_len = len(cycle[0])
            if recur_len > max_len:
                max_len = len(cycle[0])
                target_denom = i
            break

print max_len, target_denom
# the output is 982, 983

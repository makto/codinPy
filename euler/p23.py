#!/usr/bin/env python
"""
Find the sum of all the positive integers which cannot be written as the sum of two abundant numbers.
"""

from commons import divisors

abundants = [i for i in range(1,28123) if sum(divisors(i))-i > i]

#########
# the following method is too slow
#########
#result = []
#for i in range(1, 28123):
#    print i
#    half_i = i/2 + 1
#    for j in range(1, half_i):
#        if j in abundants and (i-j) in abundants:
#            break
#    else:
#        result.append(i)
#
#print sum(result)
#########

anti_result = set()
for i in abundants:
    for j in abundants:
        if i + j > 28123:
            break
        anti_result.add(i+j)

result = set(range(1, 28123)) - anti_result
print sum(result)


#!/usr/bin/env python
"""
Find the sum of all numbers that can be written as pandigital products.
"""

from itertools import permutations
from itertools import combinations

###########################
#   m1     m2       p
#  /^\   /^^^\   /^^^^^\
#  3 9 * 1 8 6 = 7 2 5 4
#      m       e
#  \___________________/
#       sequence
###########################

sequences = permutations('123456789', 9)    # All the possible sequence
seps = combinations('12345678', 2)          # The positions of * and =
seperations = []
for sep in seps:
    seperations.append(map(int, sep))

result = []
for sequence in sequences:
    sequence = ''.join(sequence)
    for m, e in seperations:
        m1 = int(sequence[:m])
        m2 = int(sequence[m:e])
        p = int(sequence[e:])
        if p in result:
            continue
        if m1 * m2 == p:
            result.append(p)

print sum(result)

# not so fast, but acceptable.

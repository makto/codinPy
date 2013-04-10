"""
if p is the perimeter of a right angle triangle, {a, b, c}, which value, for p <= 1000, has the most solutions?
"""

from collections import defaultdict
from math import sqrt

record = defaultdict(lambda:0)

for a in range(1, 999):
    for b in range(1, 999):
        if a + b >= 1000:
            break
        c = sqrt(a**2 + b**2)
        perimeter = a + b + c
        if perimeter > 1000:
            break
        if int(c) == c:
            record[perimeter] += 1

maxn = 0
maxp = None
for p, n in record.items():
    if n > maxn:
        maxn = n
        maxp = p
print maxp, maxn

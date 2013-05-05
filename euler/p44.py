"""
Pentagonal numbers are generated by the formula, Pn=n(3n-1)/2. The first ten pentagonal numbers are:
    1, 5, 12, 22, 35, 51, 70, 92, 117, 145, ...
It can be seen that P4+P7 = 22+70 = 92 = P8. However, their difference, 70-22 = 48, it not pentagonal.
Find the pair of pentagonal numbers, Pj and Pk, for which their sum and difference are pentagonal and D = |Pk-Pj| is minimised; what is the value of D?
"""

from math import sqrt

def valid(num):
    return num > 0 and int(num) == num

def is_pentagon(*nums):
    for num in nums:
        part = sqrt(1+24*num)
        if int(part) != part:
            return False
        root1, root2 = (1+part)/6, (1-part)/6
        if not any(map(valid, [root1, root2])):
            return False
    print root1, root2, nums
    return True


min_diff = float('inf')

pentagons = []
pentagons.append(1*(3*1-1)/2)

n = 1
while True:
    increment = 3*n + 1
    pentagon = pentagons[-1] + increment

    for nn, p in enumerate(pentagons[::-1]):
        diff = pentagon - p
        if diff >= min_diff:
            break
        if nn == 0 and diff >= min_diff:
            print min_diff
            exit(0)
        addi = pentagon + p
        if is_pentagon(diff, addi):
            print n, pentagon, p
            min_diff = min_diff if diff>min_diff else diff

    pentagons.append(pentagon)

    n += 1


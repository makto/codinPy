"""
What is the largest 1 to 9 pandigital that can be formed by multiplying a fixed number by 1, 2, 3, ... ?
"""

from itertools import permutations

for num in permutations('987654321'):
    num = ''.join(num)
    pos = 1
    while pos <= 4:
        first = num[:pos]
        new_num = first
        multier = 1
        while len(new_num) < 9:
            multier += 1
            second = str(int(first) * multier)
            new_num += second
        if new_num == num:
            print num, multier
            exit(0)
        pos += 1

# the answer is 932718654 (1, 2)

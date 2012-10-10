#!/usr/bin/env python
"""
Investigating combinations of English currency denominations.
"""

coins = [200, 100, 50, 20, 10, 5, 2, 1]

ways_num = 0

def get_coins(left):
    "generate the coins less than left"
    all_coins = coins[:]
    all_coins.append(left)
    all_coins.sort(reverse=True)
    pos = all_coins.index(left) + 1
    return all_coins[pos:]

def find(left, l_coins=None):
    global ways_num
    left_coins = l_coins if l_coins else get_coins(left)
    nxt = left_coins[0]

    times = 0
    while True:
        new_left = left - nxt*times
        if new_left > 0:
            if len(left_coins) == 1:
                pass
            else:
                find(new_left, left_coins[1:])
        elif new_left < 0:
            break
        else:
            ways_num += 1
            print ways_num
            break
        times += 1

find(200)
print ways_num

# it's so fast!

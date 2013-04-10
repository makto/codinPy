#!/usr/bin/env python
"""
How many letters would be needed to write all the numbers in words from 1 to 1000?
"""

# you can change the values to their length.
# eg, 3 instead of 'one', 6 instead of 'eleven', etc.
# but the difference is little.
map_dict = dict([(1, 'one'), (2, 'two'), (3, 'three'), (4, 'four'), (5, 'five'),
                 (6, 'six'), (7, 'seven'), (8, 'eight'), (9, 'nine'), (10, 'ten'),
                 (11, 'eleven'), (12, 'twelve'), (13, 'thirteen'), (14, 'fourteen'),
                 (15, 'fifteen'), (16, 'sixteen'), (17, 'seventeen'), (18, 'eighteen'),
                 (19, 'nineteen'), (20, 'twenty'), (30, 'thirty'), (40, 'forty'),
                 (50, 'fifty'), (60, 'sixty'), (70, 'seventy'), (80, 'eighty'),
                 (90, 'ninety')])

def trans(n):
    if n < 20:
        return map_dict[n]
    elif n < 100:
        if n % 10 == 0:
            return map_dict[n]
        else:
            pre = map_dict[(n/10)*10]
            suf = map_dict[n % 10]
            return pre + suf
    elif n < 1000:
        pre = map_dict[n/100]
        if n % 100 == 0:
            return pre + 'hundred'
        else:
            suf = trans(n % 100)
            return pre + 'hundred' + 'and' + suf
    else:
        return 'one' + 'thousand'

print sum([len(trans(i)) for i in xrange(1, 1001)])

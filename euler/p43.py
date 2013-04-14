"""
The number, 1406357289, is a 0 to 9 pandigital number because it is made up of each of the digits 0 to 9 in some order, but it also has a rather interesting sub-string divisibility property.
let d1 be the 1st digit, d2 be the 2nd digit and so on. In this way, we note the following:
    d2d3d4=406 is divisible by 2
    d3d4d5=063 is divisible by 3
    d4d5d6=635 is divisible by 5
    d5d6d7=357 is divisible by 7
    d6d7d8=572 is divisible by 11
    d7d8d9=728 is divisible by 13
    d8d9d10=289 is divisible by 17
Find the sum of all 0 to 9 pandigital numbers with this property.
"""

from operator import add

def mystr(num):
    num_str = str(num)
    len_str = len(num_str)
    return '0'*(3-len_str)+num_str

def unique(*strings):
    glue = reduce(add, strings)
    return len(set(glue)) == len(glue)

def to_number(*strings):
    glue = reduce(add, strings)
    for i in range(10):
        if str(i) not in glue:
            first = str(i)
            break
    return int(first+glue)

def divisible(strd, div):
    return int(strd)%div == 0

results = []

d8910 = 0
i = 0
while d8910 < 1000:
    i += 1
    d8910 = 17 * i
    strd8910 = mystr(d8910)
    if not unique(strd8910):
        continue
    j = 0
    d567 = 0
    while d567 < 1000:
        j += 1
        d567 = 7 * j
        strd567 = mystr(d567)
        if not unique(strd567,strd8910):
            continue
        strd789 = strd567[-1]+strd8910[:-1]
        strd678 = strd567[1:]+strd8910[0]
        if not divisible(strd789, 13) or not divisible(strd678, 11):
            continue
        k = 0
        d234 = 0
        while d234 < 1000:
            k += 1
            d234 = 2 * k
            strd234 = mystr(d234)
            if not unique(strd234, strd567, strd8910):
                continue
            strd456 = strd234[-1] + strd567[:-1]
            strd345 = strd234[1:] + strd567[0]
            if not divisible(strd456, 5) or not divisible(strd345, 3):
                continue
            result = to_number(strd234, strd567, strd8910)
            results.append(result)

print sum(results)

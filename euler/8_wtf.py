#!/usr/bin/env python
"""
Discover the largest product of five consecutive digits in the 1000-digit number.
The 1000-digit number are defined below
"""

number = "7316717653133062491922511967442657474235534919493496983520312774506326239578318016984801869478851843858615607891129494954595017379583319528532088055111254069874715852386305071569329096329522744304355766896648950445244523161731856403098711121722383113622298934233803081353362766142828064444866452387493035890729629049156044077239071381051585930796086670172427121883998797908792274921901699720888093776657273330010533678812202354218097512545405947522435258490771167055601360483958644670632441572215539753697817977846174064955149290862569321978468622482839722413756570560574902614079729686524145351004748216637048440319989000889524345065854122758866688116427171479924442928230863465674813919123162824586178664583591245665294765456828489128831426076900422421902267105562632111110937054421750694165896040807198403850962455444362981230987879927244284909188845801561660979191338754992005240636899125607176060588611646710940507754100225698315520005593572972571636269561882670428252483600823257530420752963450"

#########
# WTF! Digits! What does it mean by digits!!!
#########

def find_num_by_len(length):
    nums = []
    for i in xrange(1000):
        end = i + length
        if end > 1000:
            return nums
        num = number[i:end]
        if num.startswith('0'):   # incase num is started with 0
            continue
        nums.append(int(num))
    return nums

def is_consecution(num, s_set, l_set):
    num += 1
    for i in xrange(4):
        if num in s_set or num in l_set:
            num += 1
        else:
            return False
    return True

def search_loop():
    result = []
    s_nums = find_num_by_len(1000)
    for i in xrange(1000, 1, -1):
        l_nums = s_nums
        s_nums = find_num_by_len(i-1)
        for j in s_nums:
            if is_consecution(j, s_nums, l_nums):
                result.append(j)
        if result:
            return result
    return []

import time
import operator
t_a = time.time()
result = max(search_loop())
max_product = reduce(operator.mul, [result+i for i in xrange(5)])
t_b = time.time()
t_diff = t_b - t_a
print result, max_product, t_diff

#########
# if the five consecutive digits are asked to be adjacent
# then the solution would be as below.
#########

#result = {}
#
#for length in xrange(200, 0, -1):
#    for start in xrange(995):
#        tmp_len = length
#
#        p1 = start          # marks the start postion of first
#        p2 = p1 + tmp_len   # start position of second
#        p3 = p2 + tmp_len   # end position of second
#        p4 = p3 + 1         # second may be one digit more
#
#        for i in xrange(4):
#            if p3 > 999:
#                break       # no enough numbers left
#
#            pre = int(number[p1:p2])
#            lat_a = int(number[p2:p3])
#            if pre + 1 != lat_a:
#                lat_b = int(number[p2:p4])
#                if pre + 1 == lat_b:
#                    tmp_len += 1
#                else:
#                    break   # not consecutive
#
#            p1 = p2
#            p2 = p1 + tmp_len
#            p3 = p2 + tmp_len
#            p4 = p3 + 1
#
#        else:
#            first = int(number[start:start + length])
#            result[(start, length)] = first
#
#print result


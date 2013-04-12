#-*- coding: utf-8 -*-

"""
An irrational decimal fraction is created by concatenating the positive integers:
    0.123456789101112131415161718192021...
It can be seen that the 12th digit of the fractional part is 1
If dn represents the nth digit of the fractional part, find the value of the following expression:
    d1 * d10 * d100 * d1000 * d10000 * d100000 * d1000000
"""

def nth(n):
    num_of_digit = 0    # 到目前为止的总位数
    i = 0               # i+1 表示当前位段是几位数
    while True:
        base = 10 ** i  # 当前位段的第一个数
        pre_num_of_digit = num_of_digit
        num_of_digit += base*9*(i+1)   # 当前位段的位个数 

        diff = n - pre_num_of_digit    # 所求位距上个位段结束的位距离
        if diff >= 0 and n < num_of_digit:
            pre_num = base-1 + diff/(i+1)
            left = diff%(i+1)
            if left:
                rt = str(pre_num+1)[left-1]
            else:
                rt = str(pre_num)[-1]
            return int(rt)

        i += 1


result = 1
for i in range(7):
    result *= nth(10**i)

print result

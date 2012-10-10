#!/usr/bin/env python
"""
Find the sum of all the numbers that can be written as the sum of fifth powers of their digits.
"""

# There is a point, where the sum of digits will
# never catch up with the original number again.
# e.g. The minimum of 7-digits number is 1000000,
#      while the largest sum of 7 digits is 413343
#      , or (9**5)*7, which is less than 1000000.
#      which means the targets we are looking for
#      will never have digits more than 7.

# so, let's find the point, which proves to be 6 digits.
length = 2
while True:
    mini_num = 10 ** (length-1)
    maxi_sum = (9 ** 5) * length
    if maxi_sum <= mini_num:
        break
    length += 1
print length-1

# the following procedure is pretty fast.
result = []
for l in range(2, length):  # yep, we don't need to minus 1
    floor = 10**(l-1)
    cell_a = (9**5)*l+1
    cell_b = 10**l
    cell = cell_a if cell_a < cell_b else cell_b
    for n in range(floor, cell):
        digits_sum = sum([int(i)**5 for i in str(n)])
        if digits_sum == n:
            result.append(n)

print result
print sum(result)

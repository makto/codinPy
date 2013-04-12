"""
We shall say that an n-digit number is pandigital if it makes use of all the digits 1 to n exactly once. For example, 2143 is a 4-digit pandigital and is also prime.
What is the largest n-digit pandigital prime that exists?
"""

from itertools import permutations
from commons import is_prime

for n in range(9, 1, -1):
    perms = permutations(range(n, 0, -1), n)    # ensure firstly output larger ones
    for p in perms:
        str_p = [str(i) for i in p]
        int_p = int(''.join(str_p))
        if is_prime(int_p):
            print int_p
            exit(0)

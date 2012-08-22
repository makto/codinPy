#!/usr/bin/env python
"""
What is the difference between the sum of the squares and the square of the sums?
take the first one hundred natural numbers for example.
"""

def sum_of_square(n):
    return sum(map(pow, range(1,n+1), [2]*100))

def square_of_sum(n):
    return pow(sum(range(1,n+1)), 2)

print square_of_sum(100) - sum_of_square(100)

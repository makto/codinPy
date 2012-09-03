#!/usr/bin/env python
"""
What is the first term in the Fibonacci sequence to contain 1000 digits?
"""

fib_a = 1
fib_b = 1
num = 2
limit = 10 ** 999

while True:
    fib_a, fib_b = fib_b, fib_a+fib_b
    num += 1
    if fib_b >= limit:
        print fib_b, num
        break

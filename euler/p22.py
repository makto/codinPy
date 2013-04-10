#!/usr/bin/env python
"""
What is the total of all the names scores in the file of first names?
The file is named names.txt
"""

thefile = open('names.txt').read()     # a string
names = eval(thefile)           # a tuple
sorted_names = sorted(names)    # sorted list

def get_value(name):
    "the alphabeltical value for some name"
    return sum([ord(i)-64 for i in name])

total = 0
for n, i in enumerate(sorted_names):
    value = get_value(i)
    score = value * (n+1)
    total += score

print total

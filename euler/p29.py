#!/usr/bin/env python
"""
How many distinct terms are in the sequence generated by a**b for 2 <= a <= 100 and 2 <= b <= 100?
"""

terms = set()
for a in xrange(2, 101):
    for b in xrange(2, 101):
        terms.add(a**b)

print len(terms)

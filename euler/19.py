#!/usr/bin/env python
"""
How many Sundays fell on the first of the month during the twentieth century?
"""

smalls = (4, 6, 9, 11)

def is_leap(year):
    if year % 400 == 0:
        return True
    elif year % 4 == 0 and year % 100 != 0:
        return True
    return False

def days_of_month(month, year):
    if month == 2:
        if is_leap(year):
            return 29
        else:
            return 28
    elif month in smalls:
        return 30
    else:
        return 31

past_days = sum([days_of_month(m, 1900) for m in xrange(1, 13)])
total = 0
for year in xrange(1901, 2001):
    for month in xrange(1, 13):
        if (past_days+1) % 7 == 0:
            total += 1
        past_days += days_of_month(month, year)

print total

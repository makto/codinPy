#! /usr/bin/env python
# Add all the natural numbers below one thousand that are multiples of 3 or 5.

def way_1():
    result = 0
    for i in xrange(1000):
        if i % 3 == 0 or i % 5 == 0:
            result += i
    return result

def way_2():
    result = sum([i for i in xrange(1000) if i%3 == 0 or i%5 == 0])
    return result

if __name__ == '__main__':
    import time
    time_a = time.time()
    print way_1()
    time_b = time.time()
    print time_b - time_a
    time_c = time.time()
    print way_2()
    time_d = time.time()
    print time_d - time_c

# It seems that way_2 is faster than way_1

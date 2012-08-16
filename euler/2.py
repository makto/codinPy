#! /usr/bin/env python
# By considering the terms in the Fibonacci sequence whose values do not exceed four million, find the sum of the even valued terms.

def way_1():
    fibo_a = 1
    fibo_b = 2
    result = 0
    while fibo_b <= 4000000:
        if fibo_b % 2 == 0:
            result += fibo_b
        fibo_a, fibo_b = fibo_b, fibo_a+fibo_b
    return result

def way_2():
    fibo = [1, 2]
    while True:
        fibo.append(fibo[-1]+fibo[-2])
        if fibo[-1] > 4000000:
            break
    return sum([i for i in fibo if i%2==0])

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

# it's suprising that way_2 is faster than way_1

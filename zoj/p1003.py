import sys

def search(number, s_range):
    if number == 1:
        return []
    for n, i in enumerate(s_range):
        if number < i:
            break
        if number % i == 0:
            others = search(number/i, s_range[n+1:])
            if others != False:
                return [i] + others
            else:
                continue
    return False

for line in sys.stdin:
    a, b = map(int, line.split())
    higher, lower = (a, b) if a > b else (b, a)

    limit = lower+1 if lower<=100 else 101
    h_limit = higher+1 if higher <= 100 else 101
    h_valid = l_valid = False
    for start in range(2, limit):
        l_range = range(start, limit)
        l_factors = search(lower, l_range)
        if l_factors:
            l_valid = True
        else:
            continue
        #h_range = sorted(list(set(range(2,h_limit)) - set(l_factors)))
        h_range = range(2, h_limit)
        for f in l_factors:
            h_range.remove(f)
        h_factors = search(higher, h_range)
        if h_factors:
            h_valid = True
            break
    if lower == 1:
        l_valid = True
        h_factors = search(higher, range(2,h_limit))
        if h_factors:
            h_valid = True
    if l_valid and not h_valid:
        print lower
    else:
        print higher

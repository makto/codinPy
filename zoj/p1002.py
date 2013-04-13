import sys
from itertools import combinations

def is_legal(city, city_v, size, config):
    line_group = [[x[1] for x in config if x[0]==i] for i in range(size)]
    colu_group = [[y[0] for y in config if y[1]==j] for j in range(size)]
    for ln, houses in enumerate(line_group):
        h_n = len(houses)
        if h_n <= 1:
            continue
        elif h_n > 2:
            return False
        else:
            middle = city[ln][houses[0]+1:houses[1]]
            if 'X' not in middle:
                return False
    for cn, houses in enumerate(colu_group):
        h_n = len(houses)
        if h_n <= 1:
            continue
        elif h_n > 2:
            return False
        else:
            middle = city_v[cn][houses[0]+1:houses[1]]
            if 'X' not in middle:
                return False
    return True

def maxhouses(city, size):
    if size == 1 and '.' == city[0][0]:
        return 1
    spaces = [(n, m) for n, horiz in enumerate(city)
                     for m, block in enumerate(horiz) if block == '.']
    city_verti = [[city[i][j] for i in range(size)] for j in range(size)]

    result = 0
    for maxi in range(1, size*size):
        configs = combinations(spaces, maxi)
        for c in configs:
            if is_legal(city, city_verti, size, c):
                result = maxi
                break
        else:
            break
    return result
    
while True:
    n = int(sys.stdin.readline().rstrip())
    if not n:
        break
    city = []
    for i in range(n):
        city.append(list(sys.stdin.readline().rstrip()))
    print maxhouses(city, n)

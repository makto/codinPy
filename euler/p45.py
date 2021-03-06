"""
Triangle, pentagonal, and hexagonal numbers are generated by the following formulae:
    Triangle    Tn = n(n+1)/2    1, 3, 6, 10, 15, ...
    Pentagonal  Tn = n(3n-1)/2   1, 5, 12, 22, 35, ...
    Hexagonal   Tn = n(2n-1)     1, 6, 15, 28, 45, ...
It can be verified that T285 = P165 = H143 = 40755
Find the next triangle number that is also pentagonal and hexagonal.
"""

from math import sqrt

def iroot(*roots):
    "extract the integer root"
    for r in roots:
        if r > 0 and int(r) == r:
            return r
    return None

n = 285
while True:
    n += 1
    tt = n*(n+1)

    ps = sqrt(1+12*tt)
    if int(ps) == ps:
        proots = (1+ps)/6, (1-ps)/6
        p_root = iroot(*proots)
        if not p_root:
            continue
    else:
        continue

    hs = sqrt(1+4*tt)
    if int(hs) == hs:
        hroots = (1+hs)/4, (1-hs)/4
        h_root = iroot(*hroots)
        if not h_root:
            continue
    else:
        continue

    print tt/2, n, p_root, h_root
    break

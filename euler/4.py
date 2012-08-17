#!/usr/bin/env python
"""
Find the largest palindrome made from the product of two 3-digit numbers.
e.g. The largest palindrome made from the product of two 2-digit numbers is 9009 = 91 * 99.
"""

def gene_palins():
    """generate all the potential palindromes in order"""
    palins = []
    # the smallest candidate is 100*100 = 10000
    # which is 5-digit
    # the largest candidate is 999*999 = 998001
    # which is 6-digit
    for i in xrange(1, 10):
        for j in xrange(10):
            for k in xrange(10):
                palin_a = '%d%d%d%d%d' % (i,j,k,j,i)
                palin_b = '%d%d%d%d%d%d' % (i,j,k,k,j,i)
                palins.extend([eval(palin_a), eval(palin_b)])
    return sorted(palins, reverse=True)

def filter(palins):
    """pick out the largest palindromes
    that are product of two 3-digit numbers"""
    def analyze(palin):
        for i in range(100, 999):
            if palin % i == 0 and len(str(palin/i)) == 3:
                return (i, palin/i)
        return ()
    for p in palins:
        factors = analyze(p)
        if factors:
            return p, factors
    return 'NotFound'

if __name__ == '__main__':
    print filter(gene_palins())

# the result is 906609 = 913 * 993

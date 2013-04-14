#-*- coding: utf-8 -*-
"""
一种简洁的求指定列表组合的办法
使用递归，与subsets_pro类似
"""

def combinations(source, length):
    if length == 0:
        yield []
        return

    source_len = len(source)
    if length > source_len:
        yield []
    elif length == source_len:
        yield source
    else:
        for n,i in enumerate(source):
            if source_len - n < length:
                return
            for com in combinations(source[n+1:],length-1):
                yield [i]+com

source = [1,2,3,4,5]
coms = list(combinations(source, 2))
print coms
print len(coms)

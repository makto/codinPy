#-*- coding: utf-8 -*-
"""
更简洁的递归方法来生成全部子集
基本思想是，[a,SET]的子集等于SET的所有子集和SET每个子集加上a后的集合的并集
"""

def subsets(parset):
    if parset:
        head = parset.pop()
        for sub in subsets(parset):
            yield [head] + sub
            yield sub
    else:
        yield []

parset = {1,2,3,4,5}
subs = list(subsets(parset.copy()))
print subs
print len(subs)

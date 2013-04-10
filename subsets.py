#-*- coding: utf-8 -*-

"""
给定集合 test_case
输出其所有子集
"""

def getsubs(father, size):
    """获取集合 father 的
    指定长度 size 的所有子集合"""
    all_subs = []
    excludes = set()
    for i in father:
        sub = set() 
        sub.add(i)
        if len(sub) == size:
            all_subs.append(sub)
        else:
            excludes.add(i)
            new_father = father.difference(excludes)
            _sub = getsubs(new_father, size-1)
            for s in _sub:
                all_subs.append(sub.union(s))
    return all_subs

test_case = set((1,2,3,4))
test_len = len(test_case)

subsets = []
test_case_copy = test_case.copy()
for size in range(1, test_len):
    # 用内置的 itertools.combinations 更方便
    subs = getsubs(test_case_copy, size)
    subsets.extend(subs)

# 添加空集和集合本身
subsets.append(set())
subsets.append(test_case)

print subsets

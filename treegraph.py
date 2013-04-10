#! /usr/bin/env python2.7
#-*- coding: utf-8 -*-

"""

用形如(father, child)的一组 tuple 来描述结构
本程序会输出其可视化的树状结构
有 pprint 和 tprint 两种格式的输出

示例输入：
data = (('fruit','apple'),('fruit','pear'),('apple','macintosh'),
        ('pet','dog'),('pet','cat'),('pet','turtle'))

对应输出：
pet
  turtle
  dog
  cat
fruit               <<< 这是 pprint
  pear
  apple
    macintosh

┬─pet─┬─turtle
│     ├─dog
│     └─cat         <<< 这是 tprint
└─fruit─┬─pear
        └─apple───macintosh


- 输入的 tuple 不限深度，不限顺序
- 智能判断结构关系（可以尝试冗余输入、多父节点输入等）

"""

from collections import defaultdict


def mydict():
    """自动生成默认值的自定义字典
    任意深度均可"""
    return defaultdict(mydict)


class TreeGraph:
    """用字典来构造树状结构"""

    def __init__(self):
        self.dic = mydict()

    @staticmethod
    def find(dic, target):
        """在数据集dic中找到目标节点targe的所有路径"""
        all_paths = []

        for k, v in dic.items():
            if k == target:
                all_paths.append([k]) # 如果找到，则其不可能出现在
                break                 # 同一父节点的其他子节点下
            else:
                sub_paths = TreeGraph.find(v, target)
                for path in sub_paths:
                    all_paths.append([k]+path)

        return all_paths

    def add(self, key, val):
        self.key_paths = TreeGraph.find(self.dic, key)
        self.val_paths = TreeGraph.find(self.dic, val)
        self.val_del = []
        self.key_paths = self.key_paths if self.key_paths else [[key]]
        self._clean_paths()

        if self.val_paths:
            val_subs = self._get(self.val_paths[0])
        else:
            val_subs = mydict()

        for path in self.val_del:
            val_del_parent = self._get(path[:-1])
            del val_del_parent[val]

        self._pushall(val, val_subs)

        del self.key_paths
        del self.val_paths
        del self.val_del
    
    def _clean_paths(self):
        """删掉冗余的key_paths
        生成需要删除的val_paths"""
        for k_path in self.key_paths:
            k_path.insert(0, 'root')
            k_p_len = len(k_path)

            for v_path in self.val_paths:
                v_path.insert(0, 'root')
                v_p_len = len(v_path)

                if k_path == v_path[:k_p_len]:
                    self.key_paths.remove(k_path)
                    v_path.pop(0)
                    break
                if v_path[:-1] == k_path[:v_p_len-1]:
                    self.val_del.append(v_path[1:])

                v_path.pop(0)

            k_path.pop(0)

    def _pushall(self, val, val_subs):
        """将val及其子树插入到所有的key下"""
        for k_path in self.key_paths:
            key = self._get(k_path)
            key[val] = val_subs

    def _get(self, path):
        """获取指定path处的节点"""
        tree = self.dic
        for node in path:
            tree = tree[node]
        return tree


def pprint(tree, indent):
    """缩进形式的结构输出"""
    for k, v in tree.items():
        print indent+k
        if v:
            pprint(v, indent+' '*2)


import sys
def tprint(tree, indent):
    """输出 pstree 样式的树状结构"""
    l = len(tree)
    now = 1
    if indent == ' ' and l > 1:
        indent = '│'
    for k, v in tree.items():
        out = ''
        if l == 1:
            out += '──'
        else:
            if now == 1:
                out += '┬─'
            elif now == l:
                out = out + '└─'
            else:
                out = out + '├─'
        out += k
        if now == 2:
            indent = indent[:-3]
        if now != 1:
            sys.stdout.write(indent)
        if v:
            out += '─'
            sys.stdout.write(out)
            if now == 1:
                new_indent = indent + ' '*(2+len(k))# + '│'
            elif now != l:
                new_indent = indent + '│' + ' '*(2+len(k))#'│'
            elif now == l:
                new_indent = indent + ' '*(3+len(k))# + '│'
            if len(v) > 1:
                new_indent += '│'
            else:
                new_indent += ' '
            tprint(v, new_indent)
        else:
            sys.stdout.write(out+'\n')
        now += 1


# 测试数据
data = [('a','b'), ('b','c'), ('b','d'), ('c','e'), ('li','f'),
        ('f','g'), ('a','h'), ('d','x'), ('d','y'), ('f', 'z'),
        ('d','s'), ('b','u'), ('a','v')]

tree = TreeGraph()
for parent, child in data:
    tree.add(parent, child)

pprint(tree.dic, '')    # 仅有缩进的输出
tprint(tree.dic, ' ')   # pstree 样式的输出

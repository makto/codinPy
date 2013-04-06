#! /usr/bin/env python2.7
#-*- coding: utf-8 -*-

"""
删除 C 语言源文件中的注释
并统计注释行数
（同一行中多个块注释算作一行）


能够处理被续行符分割开的注释：

CASE 1:
    int a; /\
    / this is a comment
CASE 2:
    int b; //\
    this is also a comment
CASE 3:
    int c; /\
    * this is still a comment */
"""

import os
from os.path import join as dirsjoin
import shutil

C_SUFFIX = ('.h', '.c')


class LineBox:
    """行处理器
    以语义行为处理单元
    即注释块、字符数组均完整，切无续行符"""
    
    def __init__(self):
        self.lines = []      # 语义上联系在一起的行
        self.seps = []       # 标识各行中注释的始末位置
        self.quote = 0       # 是否在双引号中
        self.block = False   # 是否在块注释中
        self.lcmmt = False   # 是否在行注释中
        self.conti = False   # 是否有续行符

        self._bslash = False # 上一个字符是否为反斜线
        self._slash = False  # 上一个字符是否为斜线
        self._star = False   # 上一个位置是否为星号

    def _parse(self, line):
        "分析新加入的行内容"
        if line.endswith('\\'):
            self.conti = True
            line = line[:-1]
        else:
            self.conti = False
        seps = self.seps[-1]
        for idx, char in enumerate(line):
            if not self.cmmt(): 
                if char == '"' and not self._bslash:
                    self.quote = (self.quote + 1) % 2
            if not self.quote:
                if char == '*' and self._slash and not self.cmmt()\
                               and idx-1 not in seps:
                    self.block = True
                    if idx == 0:
                        self.seps[-2].append(-3)
                    else:
                        seps.append(idx-1)
                if char == '/' and self._star and self.block\
                               and idx-2 not in seps:
                    self.block = False
                    if len(seps) == 0:
                        seps.append(0)
                    seps.append(idx)
                if char == '/' and self._slash and not self.cmmt():
                    self.lcmmt = True
                    if idx == 0:
                        self.seps[-2].append(-3)
                    elif idx == 1:
                        seps.append(idx-1)
                    else:
                        seps.extend([idx-1, -2]) # hack
            self._bslash = True if char == '\\' else False
            self._slash = True if char == '/' else False
            self._star = True if char == '*' else False
        if self.cmmt() and len(seps) == 0:
            seps.append(0)
        if not self.conti:
            self.lcmmt = False

    def add(self, line):
        "向语义行中添加一行"
        self.lines.append(line)
        self.seps.append([])    # 保证seps和lines等长且一一对应
        self._parse(line.rstrip())

    def complete(self):
        """语义上的一行已经完整
        无未配对的引号，续行符，块注释等"""
        return not(self.quote or self.block or self.conti)
    
    def cmmt(self):
        "for convenience"
        return self.block or self.lcmmt

    def getlines(self):
        """返回删除注释后的行内容
        必须确保语义行完整"""
        assert self.complete()
        newlines = []
        for lines, seps in zip(self.lines, self.seps):
            newline = list(lines)
            for start, stop in map(None, seps[::2], seps[1::2]):
                if stop == None:
                    del newline[start:]
                else:
                    del newline[start:stop+1]
            newline = ''.join(newline)
            newlines.append(newline)
        return newlines

    def clear(self):
        """重新初始化，准备处理下一个语义行
        同时返回本段的注释行数"""
        lines_with_cmmt = [sep for sep in self.seps if sep]
        self.__init__()
        return len(lines_with_cmmt)


def del_comment(origin, fresh):
    """删除文件中的注释，并写入新的文件
     返回注释行的数目"""
    linebox = LineBox()
    cmmt_count = 0
    for l in origin:
        linebox.add(l)
        if linebox.complete():
            lines = linebox.getlines()
            fresh.writelines(lines)
            cmmt_count += linebox.clear()
    return cmmt_count


if __name__ == '__main__':
    print '请输入项目的绝对路径:'
    print '(去除注释后的项目文件将保存在`name_nc`目录下)'
    while True:
        src_path = raw_input()
        if os.path.isdir(src_path):
            break
        else:
            print '无此目录，请重新输入:\n'
    #for convenience
    #src_path = r'/home/zhongqi/resources/src/'

    root_path, prj_dir = os.path.split(src_path.rstrip('/'))
    prj_nc_dir = prj_dir + '_nc/'
    new_path = dirsjoin(root_path, prj_nc_dir)

    os.mkdir(new_path)

    print '-'*30

    l = len(src_path)
    for root, dirs, files in os.walk(src_path):
        new_root = dirsjoin(new_path, root[l:])

        # 复制文件夹
        for d in dirs:
            new_d = dirsjoin(new_root, d)
            os.mkdir(new_d)

        # 复制文件
        for f in files:
            f_path = dirsjoin(root, f)
            f_path_new = dirsjoin(new_root, f)
            # c 源文件要先删除注释
            if f.endswith(C_SUFFIX):
                with open(f_path, 'r') as origin:
                    with open(f_path_new, 'w') as fresh:
                        cmmt_count = del_comment(origin, fresh)
                print "%s: %s" % (f_path, cmmt_count)
            # 非 c 源文件直接拷贝
            else:
                shutil.copy(f_path, f_path_new)


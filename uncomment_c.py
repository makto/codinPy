#! /usr/bin/env python2.7
#-*- coding: utf-8 -*-

"""
删除 C 语言源文件中的注释
并统计每个文件中包含注释的行数

能够处理被续行符分割开的特殊情况：

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
    """行处理器，以语义行为处理单元
    即注释块、字符数组均完整，末尾无续行符的一个段落"""
    
    def __init__(self):
        self.lines = []         # 语义上联系在一起的行
        self.seps  = []         # 标识各行中注释的始末位置
        self.quote = 0          # 是否在双引号中
        self.block = False      # 是否在块注释中
        self.lcmmt = False      # 是否在行注释中
        self.conti = False      # 是否有续行符

        self._bslash = False    # 上一个字符是否为反斜线
        self._slash  = False    # 上一个字符是否为斜线
        self._star   = False    # 上一个位置是否为星号

    def _parse(self, line):
        """分析新加入的行内容"""

        # 判断续行符
        if line.endswith('\\'):
            self.conti = True
            line = line[:-1]
        else:
            self.conti = False

        seps = self.seps[-1]
        for idx, char in enumerate(line):
            # 判断字符数组
            if not self.cmmt(): 
                if char == '"' and not self._bslash:
                    self.quote = (self.quote + 1) % 2

            if not self.quote:
                # 块注释是否开始
                if char == '*' and self._slash and not self.cmmt()\
                               and idx-1 not in seps:
                    self.block = True
                    if idx == 0:
                        self.seps[-2].append(-3)
                    else:
                        seps.append(idx-1)
                # 块注释是否结束
                if char == '/' and self._star and self.block\
                               and idx-2 not in seps:
                    self.block = False
                    if len(seps) == 0:
                        seps.append(0)
                    seps.append(idx)
                # 行注释是否开始
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

        # 是否整行为注释
        if self.cmmt() and len(seps) == 0:
            seps.append(0)
        # 行注释是否结束
        if not self.conti:
            self.lcmmt = False

    def add(self, line):
        """向语义行中添加一行"""
        self.lines.append(line)
        self.seps.append([])    # 保证seps和lines等长且一一对应
        self._parse(line.rstrip())

    def complete(self):
        """语义上的一行已经完整
        无未配对的引号，续行符，块注释等"""
        return not(self.quote or self.block or self.conti)
    
    def cmmt(self):
        """for convenience"""
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

    def count_and_clear(self):
        """重新初始化，准备处理下一个语义行
        同时返回本段的注释行数"""
        lines_with_cmmt = [sep for sep in self.seps if sep]
        self.__init__()
        return len(lines_with_cmmt)


def count_del_cmmt(origin, fresh):
    """删除文件中的注释，并写入新的文件
     返回注释行的数目"""
    linebox = LineBox()

    cmmt_count = 0
    for l in origin:
        linebox.add(l)
        # 如果语义行已经完整，则写入
        # 否则继续读入下一行
        if linebox.complete():
            lines = linebox.getlines()
            fresh.writelines(lines)
            cmmt_count += linebox.count_and_clear()

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

    # 为去除注释的文件新建目录
    root_path, prj_dir = os.path.split(src_path.rstrip('/'))
    new_path = dirsjoin(root_path, prj_dir+'_nc/')
    os.mkdir(new_path)

    src_path = src_path if src_path.endswith('/') else src_path + '/'

    # 注释行数统计到 log 中
    log_path = dirsjoin(root_path, prj_dir+'.log')
    log = open(log_path, 'w')

    print '-'*30

    l = len(src_path)
    cmmt_total = 0

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
                        cmmt_count = count_del_cmmt(origin, fresh)
                # 记录日志
                rel_path = f_path.replace(src_path, '')
                log_data = "%s: %s" % (rel_path, cmmt_count)
                print log_data
                log.write(log_data+'\n')
                cmmt_total += cmmt_count
            # 非 c 源文件直接拷贝
            else:
                shutil.copy(f_path, f_path_new)

    close_line = '\n项目总注释行数%s\n' % cmmt_total
    print close_line
    log.write(close_line)
    log.close()

    print '处理完毕，结果记录在%s文件中' % log_path


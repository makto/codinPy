#! /usr/bin/env python2.7
#-*- coding: utf-8 -*-

"""
监听本地端口1234
输出警报信息到控制台
"""

from BaseHTTPServer import HTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler
from multiprocessing import Pipe
from threading import Thread
from collections import defaultdict
from urllib import unquote_plus
import json

ADDRESS = ('127.0.0.1', 1234)

# 创建两个管道
# 发送者均在服务器端
# 接受者均在判断 spam 的另一个线程
RECEIVER, NOTIFIER = Pipe()   # 通知spam策略
ACCEPTER, SENDER   = Pipe()   # 传送用户请求数据


class UserRequestHandler(BaseHTTPRequestHandler):

    def do_PUT(self):
        """通知SPAM服务更新策略"""
        data_len = int(self.headers['Content-Length'])
        data = self.rfile.read(data_len)
        data = unquote_plus(data)
        tactic_dict = json.loads(data)
        new_tactic = (tactic_dict['time_span_limit'],
                      tactic_dict['num_limit'],
                      tactic_dict['content_limit'])

        NOTIFIER.send(new_tactic)

        self.send_response(200)

    def do_POST(self):
        """处理用户实时请求"""
        data_len = int(self.headers['Content-Length'])
        data = self.rfile.read(data_len)
        data = unquote_plus(data)
        req_dict = json.loads(data)

        # 交给管道另一端的线程去处理
        SENDER.send(req_dict)

        self.send_response(200)


def alarmer(receiver, accepter):
    """做SPAM检查的线程"""

    action_mapping = {'answer':  u'回答',
                      'ask':     u'提问',
                      'comment': u'评论',}
    # record 中记录某个用户某种操作
    # 在时间和内容两个维度上的信息
    # 结构为：{'user':{'ask':{'content':['c1','c2']}}}
    # 实际应用中可用Redis等内存数据库读写
    record = defaultdict(lambda: defaultdict(
                                 lambda: defaultdict(list)))

    # tactic 中记录spam策略
    # 实际应用中从数据库中读写
    tactic = (60, 10, 10)
    time_span_limit, num_limit, content_limit = tactic

    while True:
        # 获取并更新 spam 策略
        new_tactic = None
        while receiver.poll():  # 保证获取到最新的策略
            new_tactic = receiver.recv()
        if new_tactic:
            tactic = new_tactic
            time_span_limit, num_limit, content_limit = new_tactic

        # 获取用户请求
        try:
            req_dict = accepter.recv()
        except EOFError:
            break
        user = req_dict.pop('user')
        action = req_dict.pop('action')
        action_name = action_mapping[action]

        # 记录用户请求
        time_list    = record[user][action]['time']
        content_list = record[user][action]['content']
        time_list.append(req_dict['time'])
        content_list.append(req_dict['content'])

        # 判断是否为spam
        if len(time_list) >= num_limit:
            del time_list[:-num_limit]
            time_span = time_list[num_limit-1] - time_list[0]
            if time_span < time_span_limit:
                print u'%s,"频繁%s"' % (user, action_name)
                del time_list[:]
            else:
                time_list.pop(0)
        if len(content_list) >= content_limit:
            del content_list[:-content_limit]
            if len(set(content_list)) == 1:
                print u'%s,"重复%s"' % (user, action_name)
                del content_list[:]
            else:
                content_list.pop(0)


alarm_thread = Thread(target=alarmer, args=(RECEIVER, ACCEPTER))
alarm_thread.start()

httpd = HTTPServer(ADDRESS, UserRequestHandler)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    httpd.server_close()
    SENDER.close()  # 通知 alarm 线程关闭

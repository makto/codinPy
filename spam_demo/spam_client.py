#! /usr/bin/env python2.7
#-*- coding: utf-8 -*-

"""
多线程模拟用户请求
向本地端口1234 POST JSON格式数据 
"""

from urllib import urlopen, quote_plus
from threading import Thread
import random
import time
import json

# 定义了三种用户类型
# spammer_a ：连续发重复内容
# spammer_b ：动作频率较高
# normal    ：正常用户
USER_TYPES = ('spammer_a', 'spammer_b', 'normal')
ACTIONS = ('answer', 'ask', 'comment')
URI = r'http://127.0.0.1:1234'


def simu_user():
    """模拟单个用户的请求行为
    """
    user_type = random.choice(USER_TYPES)
    user_id = str(random.randint(0, 1000))
    user_name = user_type + user_id
    print user_name # 输出到控制台，用来检查服务器输出

    if user_type != 'normal':
        action = random.choice(ACTIONS)

    while True:
        req_time = int(time.time())

        # 控制发帖类型和内容
        if user_type == 'spammer_a':
            content = 'same content'
        else:
            content = str(req_time) # 用时间戳来代表不同的发帖内容
        if user_type == 'normal':
            action = random.choice(ACTIONS)

        # 控制发帖的时间间隔
        if user_type == 'spammer_b':
            sleep_time = 3
        else:
            sleep_time = 10

        req_dict = {'user':    user_name,
                    'action':  action,
                    'content': content,
                    'time':    req_time}
        req_data = json.dumps(req_dict)
        urlopen(URI, quote_plus(req_data)).read()

        time.sleep(sleep_time)


print '以下用户发起请求：\n'

# 并发10个用户请求
for i in range(10):
    thread = Thread(target=simu_user)
    thread.daemon = True
    thread.start()

time.sleep(1)
print '回车以终止请求……'
raw_input()

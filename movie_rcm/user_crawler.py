#-*- coding: UTF-8 -*-

import urllib2, urllib
import json
import redis
import time

#数据库设计，采用Redis
#均为集合(set)结构
rd = redis.Redis(host='127.0.0.1', port=6379, db=0)
db_todo = 'USRE::TODO'          #待抓取用户
db_done = 'USER::DONE'          #已抓取过的用户
db_result = 'USER::RESULT'      #抓取到的用户

#豆瓣API
API = r'http://api.douban.com/people/%s/contacts?'
API_PARAS = {
    'start-index' : 1,
    'max-results' : 50,
    'alt' : 'json',
    'apikey' : API_KEY,
}

TIME_1st = 0    #第一次调用API的时间
API_TIMES = 0   #调用API的次数

def init_db():
    "use this only once!"
    rd.sadd(db_todo, 'candyhorse')
    rd.sadd(db_done, 'notexists')
    rd.sadd(db_result, 'candyhorse')
    print 'OK!'

def crawl_10000():
    "抓取用户id，直到db_result数量超过一万"
    break_case = 'LOL'
    while True:
        #初始化API参数
        API_PARAS['start-index'] = 1

        #取出要抓取的用户
        user = rd.spop(db_todo)
        if not user:
            break_case = 'no user to crawl=='
            break       #todo为空，没有用户可抓了，退出循环
        if rd.sismember(db_done, user):
            continue    #user在done中，说明已经抓取过，跳出本次循环

        #抓取用户关注信息的第一页
        users_data = get_data(user)
        total_num = users_data["openSearch:totalResults"]["$t"]
        contacts = users_data["entry"]
        save_to_db(contacts)

        #如果关注列表超过一页，则继续处理剩余页
        if total_num > 50:
            while True:
                API_PARAS['start-index'] += 50

                users_data = get_data(user)
                contacts = users_data["entry"]
                save_to_db(contacts)

                if len(contacts) < 50:
                    break   #已经到最后一页，跳出

        #将抓去过的用户记录进db_done
        rd.sadd(db_done, user)

        if rd.scard(db_result) > 10000:
            break_case = 'more than 10000!'
            break       #已抓取用户超过一万，则退出

    print break_case

### util functions ###
def get_data(user):
    "调用豆瓣API获取数据"
    #限制API调用频次，防止被豆瓣封禁
    if API_TIMES == 0:
        TIME_1st = time.time()
    elif API_TIMES == 38:
        time_past = time.time() - TIME_1st
        print "%s开始，经过%s秒结束" % (trans_time(TIME_1st), time_past)
        if time_past < 60:
            time.sleep(int(60 - time_past) + 1)
        API_TIMES = -1

    json_data = urllib2.urlopen(API % user + urllib.urlencode(API_PARAS)).read()
    API_TIMES += 1
    return json.loads(json_data)

def save_to_db(contacts):
    "将用户存入待抓取列表和抓取到列表"
    for contact in contacts:
        user_name = contact["db:uid"]["$t"]
        rd.sadd(db_result, user_name)
        rd.sadd(db_todo, user_name)

def trans_time(t):
    "将时间转换为可读形式"
    return time.strftime("%H:%M:%S", time.localtime(t))
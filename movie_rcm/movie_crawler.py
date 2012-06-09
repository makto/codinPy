#-*- coding: UTF-8 -*-

import time
import json
import urllib2, urllib

import redis
from oauth import API_KEY

from user_crawler import db_result          #user_crawler中抓取的用户
#db_result_backup = 'USER::RESULT::BACKUP'   #备份db_result

#数据库设计，采用Redis
rd = redis.Redis(host='127.0.0.1', port=6379, db=0)
db_user_movie = 'USER::%s::MOVIE'       #单个用户对各个电影的评分，hash结构
#db_movie_user = 'MOVIE::%s::USER'   #单部电影的所有用户评分，hash结构
db_users = 'USERS::VALID'               #看过100以上电影的用户，set结构
#db_movies = 'MOVIES::ALL'           #被统计到的电影全集，set结构
db_movie_info = 'MOVIE::ID::NAME'       #电影的id与name对，hash结构
db_user_watched = 'USER::MOVIE::NUM'    #用户看过的电影数，hash结构
db_user_failed = 'USER::FAILED'         #抓取出错的用户，集合

#豆瓣API | 查询用户收藏信息
API = r'http://api.douban.com/people/%s/collection?'
API_PARAS = {
    'cat' : 'movie',
    'status' : 'watched',
    'start-index' : 1,
    'max-results' : 50,
    'alt' : 'json',
    'apikey' : API_KEY,
}

API_TIMES = 0
TIME_1st = 0    #记录API调用频次

def crawl_all():
    """抓取db_result中所有用户的电影评分信息
    筛去看过电影少于100部的用户
    """
    users = rd.smembers(db_result)
    for user in users:
        if rd.sismember(db_users, user):
            continue
        while True:
            try:
                user_data = get_data(user)
                break
            except:
                print "HTTPError happens at %s! start-index : %s" % (user, 50)
        try:
            total_watched = int(user_data['opensearch:totalResults']['$t'])
        except:
            print "read %s total_watched wrong" % user
            rd.sadd(db_user_failed, user)
            continue

        movie_ratings = user_data['entry']
        rd.hset(db_user_watched, user, total_watched)
        if total_watched < 100:
            continue            #观看少于100部，则认为此用户无效
        rd.sadd(db_users, user)
        save_to_db(user, movie_ratings)

        #处理翻页的情况
        while True:
            API_PARAS['start-index'] += 50
            while True:
                try:
                    user_data = get_data(user)
                    break
                except:
                    print "HTTPError2 happens at %s! start-index : %s" % (user, API_PARAS['start-index'])
            try:
                movie_ratings = user_data['entry']
            except:
                print "user: %s, start: %s" % (user, API_PARAS['start-index'])
                rd.sadd(db_user_failed, user)
                break
            save_to_db(user, movie_ratings)
            if len(movie_ratings) < 50:
                break

        API_PARAS['start-index'] = 50       #这个应该是1，属于失误，导致每个用户少被统计50部电影

    print "all well done!"

### util functions ###
def get_data(user):
    "调用豆瓣API获取数据"
    #限制API调用频次，防止被豆瓣封禁
    global API_TIMES, TIME_1st
    if API_TIMES == 0:
        TIME_1st = time.time()
    elif API_TIMES == 38:
        time_past = time.time() - TIME_1st
        print "%s start, %s secs later finished 40, now %s" % (trans_time(TIME_1st), time_past, user)
        if time_past < 60:
            time.sleep(int(60 - time_past) + 1)
        API_TIMES = -1
    
    json_data = urllib2.urlopen(API % user + urllib.urlencode(API_PARAS)).read()

    API_TIMES += 1
    return json.loads(json_data)

def save_to_db(user, movie_ratings):
    for mr in movie_ratings:
        try:
            movie_name = mr['db:subject']['title']['$t']
            movie_id = mr['db:subject']['id']['$t'].split(r'/')[-1]
            rating = mr['gd:rating']['@value']
        except KeyError:
            continue

        rd.hset(db_user_movie % user, movie_id, rating)
        rd.hsetnx(db_movie_info, movie_id, movie_name)

def trans_time(t):
    "将时间转换为可读形式"
    return time.strftime("%H:%M:%S", time.localtime(t))

if __name__ == '__main__':
    crawl_all()
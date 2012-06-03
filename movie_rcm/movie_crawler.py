#-*- coding: UTF-8 -*-

import redis
from oauth import API_KEY

#数据库设计，采用Redis
rd = redis.Redis(host='127.0.0.1', port=6379, db=0)
db_user_movie = 'USER::%sMOVIE'   #单个用户对各个电影的评分，hash机构
db_movie_user = 'MOVIE::USER'   #单部电影的所有用户评分，hash结构
db_users = 'USERS::VALID'       #看过100以上电影的用户，set结构
db_movies = 'MOVIES::ALL'       #被统计到的电影全集，set结构

#豆瓣API | 查询用户收藏信息
API = r'http://api.douban.com/people/%s/collection'
API_PARAS = {
    'cat' : 'movie',
    'status' : 'watched',
    'start-index' : 1,
    'max-results' : 1,
    'alt' : 'json',
    'apikey' : API_KEY,
}


def main():
    #连接到数据库
    db = sqlite3.connect('ratings.db')
    c = db.cursor()
    #获取豆瓣电影数据
    total = 0       #已获取的有效数据
    while True:
        data = urllib2.urlopen()


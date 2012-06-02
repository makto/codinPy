#-*- coding: UTF-8 -*-

import urllib2
import sqlite3

from oauth import API_KEY

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


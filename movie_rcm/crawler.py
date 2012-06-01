import urllib2
import sqlite3

API = r'http://api.douban.com/people/%s/collection'
API_PARAS = {
    cat = 'movie',
    status = 'movie:watched',
    start-index = ''
}

def main():
    #连接到数据库
    db = sqlite3.connect('ratings.db')
    c = db.cursor()
    #获取豆瓣电影数据
    total = 0       #已获取的有效数据
    while True:
        data = urllib2.urlopen()
#-*- coding: UTF-8 -*-

"""
这部分代码用来做中间数据转换
"""

import redis

rd = redis.Redis(host='127.0.0.1', port=6379, db=0)

from user_crawler import db_result
db_user_watched = 'USER::MOVIE::NUM'    #db_result中所有用户看过的电影数，hash结构

db_users = 'USERS::VALID'               #看过100以上电影的基础用户集，set结构
db_user_movie = 'USER::%s::MOVIE'       #db_users中单个用户对各个电影的评分，hash结构

db_movie_info = 'MOVIE::ID::NAME'       #db_users中用户看过的电影的id与name对，hash结构

db_valid_users = 'USERS::REAL::VALID'   #评分电影大于100部的用户集合
db_user_rated = 'USERS::RATED::NUM'     #db_users中每个用户评过分的电影的数量, new

#数据库设计
db_movie_user = 'MOVIE::%s::USER'       #单部电影的所有用户评分，hash结构，new
#db_movies = 'MOVIES::ALL'               #被统计到的电影全集，set结构，new

db_valid_movies = 'MOVIES::REAL::VALID'     #评分人数超过50的电影集合, set
db_movie_watched = 'MOVIES::WATCHED::NUM'   #db_movie_info中所有电影的评分过的用户数, new

def gene_all_movie_ratings():
    """生成所有电影的用户评分信息
    即db_movie_user"""
    all_users = rd.smembers(db_result)  #又是一个失误，应该用db_users，还好不影响
    for user in all_users:
        user_ratings = rd.hgetall(db_user_movie % user)     #所得为dict类型
        for movie, rating in user_ratings.items():
            rd.hset(db_movie_user % movie, user, rating)

def gene_user_rated_num():
    """生成基础用户评分过电影的数量，以及有效用户集合
    即db_user_rated和db_valid_users"""
    basic_users = rd.smembers(db_users)
    for user in basic_users:
        rated_num = rd.hlen(db_user_movie % user)
        if int(rated_num) >= 100:
            rd.sadd(db_valid_users, user)
        rd.hset(db_user_rated, user, rated_num)

def gene_movie_watched_num():
    """生成基础电影评分用户的数量，以及有效电影集合
    即db_valid_movies和db_movie_watched"""
    movie_ids = rd.hkeys(db_movie_info)
    for m_id in movie_ids:
        watched_num = rd.hlen(db_movie_user % m_id)
        if watched_num >= 50:
            rd.sadd(db_valid_movies, m_id)
        rd.hset(db_movie_watched, m_id, watched_num)

def gene_crawl_info():
    "生成抓取结果的统计数据"
    user_pool_size = rd.scard(db_result)
    user_basic_size = rd.scard(db_users)
    user_valid_size = rd.scard(db_valid_users)
    #basic用户评过分的电影的数量分布
    #pool用户看过的电影的数量分布
    movie_basic_size = rd.hlen(db_movie_info)
    movie_valid_size = rd.scard(db_valid_movies)
    #basic电影评过分的用户数量的分布
    print u"""统计信息如下：
    用户池大小: %s
    基础用户数: %s
    有效用户数: %s
    基础电影数: %s
    有效电影数: %s
    """.encode('gbk') % (user_pool_size, user_basic_size, user_valid_size,
        movie_basic_size, movie_valid_size)


if __name__ == '__main__':
    #gene_all_movie_ratings()
    #print "all movie ratings generated!"
    #gene_user_rated_num()
    #print "all valid user rated num generated!"
    #gene_movie_watched_num()
    #print "all valid movie watched num generated!"
    gene_crawl_info()
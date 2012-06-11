#-*- coding: UTF-8 -*-

"""
这部分代码用来计算相似用户，并生成最终推荐列表
"""

import redis
from math import sqrt

db_movie_info = 'MOVIE::ID::NAME'
db_movie_user = 'MOVIE::%s::USER'
db_user_movie = 'USER::%s::MOVIE'
db_valid_users = 'USERS::REAL::VALID'
db_cacus_user = 'USERS::CACUS'          #用来存储与目标用户交集大于30的用户
db_simi_rank = 'USERS::SIMI::RANK'      #用来保存与目标用户的相似度值及排名,sorted set结构
db_simi_valid = 'USERS::SIMI::VALID'    #pearson相关度介于0.5和1之间的用户
db_final1 = 'FINAL::MOVIE::RATE'        #每部推荐电影的推荐评分
db_final2 = 'FINAL::MOVIE::NUM'         #每部推荐电影的评分人数
db_final = 'FINAL::RANK'                #将db_final1转换为有序集格式

rd = redis.Redis(host='127.0.0.1', port=6379, db=0)
target_user = 'candyhorse'

def final_rank():
    """存储和显示推荐列表前50的电影、预测评分、评分人数"""
    #all_rcmd = rd.hgetall(db_final1)
    #for i,j in all_rcmd.items():
    #    rd.zadd(db_final, i, j)
    top = rd.zrevrange(db_final, 0, -1, withscores=True)
    print "%-10s | %-60s | %-10s | %-10s" % ('movie_id', 'movie_name', 'rating', 'raters_num')
    count = 0
    for movie,rate in top:
        rater = rd.hget(db_final2, movie)
        if int(rater) < 11:
            continue
        if rate < 5:
            break
        name = rd.hget(db_movie_info, movie)
        name = unicode(name, 'utf-8', 'replace').encode('gbk', 'replace')
        #rater = rd.hget(db_final2, movie)
        print "%-10s | %-60s | %-10.5f | %-10s" % (movie, name, rate, rater)
        count += 1
    print count

def show_num(n, m):
    """显示评分人数大于等于n的电影数
    以及评分超过m的电影数"""
    all_num = rd.hvals(db_final2)
    all_movie = rd.hvals(db_final1)
    n_num = [num for num in all_num if int(num) >= n]
    n_movie = [m_n for m_n in all_movie if float(m_n) >= m]
    print len(n_num), len(n_movie)

def filter():
    "返回电影推荐列表"
    def gene_simi_valid():
        valid = rd.zrangebyscore(db_simi_rank, 0.5, 1)
        rd.sadd(db_simi_valid, *valid)
    gene_simi_valid()

    def get_movie_base():
        "返回所有target user没看过的电影"
        t_movies = set(rd.hkeys(db_user_movie % target_user))
        movie_base = set([])
        for user in rd.smembers(db_simi_valid):
            u_movies = set(rd.hkeys(db_user_movie % user))
            movie_base = movie_base.union(u_movies.difference(t_movies))
        return movie_base
    movies = get_movie_base()

    def ava(user):
        sum_u = sum([int(r) for r in rd.hvals(db_user_movie % user)])
        return sum_u * 1.0 / rd.hlen(db_user_movie % user)
    ava_t = ava(target_user)
    print ava_t
    print len(movies)

    def rate_num(movie):
        users = rd.smembers(db_simi_valid)
        raters = [u for u in users if rd.hexists(db_movie_user % movie, u)]
        #if len(raters) < 10:
        #    return 0, 0
        def rating(user, movie):
            return int(rd.hget(db_user_movie % user, movie))
        sum1 = sum([(rating(u, movie) - ava(u)) * rd.zscore(db_simi_rank, u) for u in raters])
        sum2 = sum([rd.zscore(db_simi_rank, u) for u in raters])
        rate = ava_t + (sum1 / sum2)
        return rate, len(raters)
    loop_num = 0
    for m in movies:
        rate, num = rate_num(m)
        #if rate == 0 and num == 0:
        #    continue
        rd.hset(db_final1, m, rate)
        rd.hset(db_final2, m, num)
        loop_num += 1
        print "ok : %s" % loop_num
    print "all done"

def simi_rank():
    "根据相似度对用户进行排序"
    cacus_users = rd.smembers(db_cacus_user)
    for user in cacus_users:
        simi_value = pearson(target_user, user)
        print "%s, %s" % (user, simi_value)
        rd.zadd(db_simi_rank, user, simi_value)     #redis-py的官方文档有误

def pearson(t_user, user):
    """pearson相关度计算函数"""
    def ava_common(user1, user2):
        """计算用户的评分均值 && 评分交集"""
        user1_movie = set(rd.hkeys(db_user_movie % user1))
        user2_movie = set(rd.hkeys(db_user_movie % user2))
        common_movies = user1_movie.intersection(user2_movie)
        common_num = len(common_movies)
        user1_ava = sum([int(rd.hget(db_user_movie % user1, movie)) for movie in common_movies]) / common_num
        user2_ava = sum([int(rd.hget(db_user_movie % user2, movie)) for movie in common_movies]) / common_num
        return user1_ava, user2_ava, common_movies
    t_ava, u_ava, common_movies = ava_common(t_user, user)

    def rate(user, movie):
        return int(rd.hget(db_user_movie % user, movie))
    sum1 = sum([(rate(t_user, m)-t_ava)*(rate(user, m)-u_ava) for m in common_movies])
    sum2 = sum([pow(rate(t_user, m)-t_ava, 2) for m in common_movies])
    sum3 = sum([pow(rate(user, m)-u_ava, 2) for m in common_movies])

    return sum1 / (sqrt(sum2) * sqrt(sum3))


def same_count(n, save=False):
    """计算与目标用户有n个相同评分电影的用户数
    save为false时仅是为了调试"""
    target_movies = rd.hkeys(db_user_movie % target_user)
    cacus_num = 0
    for user in rd.smembers(db_valid_users):
        same_num = 0
        for movie in target_movies:
            if rd.hexists(db_user_movie % user, movie):
                same_num += 1
        if same_num > n:
            cacus_num += 1
            if save:
                rd.sadd(db_cacus_user, user)
    print cacus_num
    if save:
        print "save done! %s" % rd.scard(db_cacus_user)

if __name__ == '__main__':
    #same_count(30)
    #same_count(30, save=True)
    #simi_rank()
    #filter()
    #show_num(10, 6)
    final_rank()
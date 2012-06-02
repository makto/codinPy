#-*- coding: UTF-8 -*-

from douban import client

#client信息
API_KEY = '065a5060be3b792f130ef1223ab26b8d'
API_KEY_SECRET = '9b59f288735dc9ce'
#授权过的一个备用token
TOKEN = 'f07525909b9fae9dd15f70b1d2df0bd7'
TOKEN_SECRET = '70d2aca1d5f1c57e'

def get_access_token():
    """
    获取用户授权的access token信息
    """
    #初始化获取access token的客户端
    auth_client = client.OAuthClient(key=API_KEY, secret=API_KEY_SECRET)
    auth_client.login()     #跳转到浏览器进行验证

    #access token及access token secret
    print auth_client.token.key
    print auth_client.token.secret

def cud_acts(api_url, token=None, secret=None):
    """
    增删改操作需要通过oauth流程访问
    """
    #若没提供token信息，则使用备用的token
    if not token or not secret:
        token = TOKEN
        secret = TOKEN_SECRET
    
    db_client = client.OAuthClient(key=API_KEY, secret=API_KEY_SECRET)  #标识owner对client的授权信息
    db_client.login(key=token, secret=secret)                           #标识client的信息
    #访问受限资源
    data = db_client.access_resource('GET', api_url).read()
    return data

if __name__ == '__main__':
    pass

import urllib2

API_KEY = '065a5060be3b792f130ef1223ab26b8d'
KEY_SECRET = '9b59f288735dc9ce'

def get_request_token_a():
    url = r'http://www.douban.com/service/auth/request_token'
    paras = {
        'oauth_consumer_key' : API_KEY,
        'oauth_signature_method' : 'HMAC-SHA1',
        'oauth_signature' : ,
        'oauth_timestamp' : ,
        'oauth_nonce' : 
        }
    suffix = urllib.urlencode(paras)
    urllib.urlopen(url + )
    return

def get_request_token_b():
    return

def get_access_token():
    return
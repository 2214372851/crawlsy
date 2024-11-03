import datetime

import jwt
from django.conf import settings
from django.core.cache import caches
from rest_framework.exceptions import NotAuthenticated

from apps.User.models import UserModel


def make_token(out_time, uid):
    access_dic = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=out_time),
        'iat': datetime.datetime.utcnow(),
        'iss': settings.TOKEN_ISS,
        'data': {
            'uid': str(uid)
        }
    }
    return jwt.encode(access_dic, settings.SECRET_KEY, algorithm='HS256')


def login_token(user: UserModel):
    """
    获取token存入缓存
    :param user: Django model user data
    :return token: user token
    """
    if not user: raise NotAuthenticated(detail='未查询到该用户')
    uid = user.uid
    access_token = make_token(settings.ACCESS_TOKEN_OUT_TIME, uid)
    refresh_token = make_token(settings.REFRESH_TOKEN_OUT_TIME, uid)
    access_cache = caches['access_token']
    refresh_cache = caches['refresh_token']
    access_cache.set(str(uid), access_token, timeout=settings.ACCESS_TOKEN_OUT_TIME)
    refresh_cache.set(str(uid), refresh_token, timeout=settings.ACCESS_TOKEN_OUT_TIME)
    return access_token, refresh_token


def verify_token(token):
    """
    验证token是否正确
    :param token: user request token
    :return payload/False: token data/verify lose
    """
    if not token: raise NotAuthenticated(detail='未携带身份信息')
    payload = jwt.decode(token, settings.SECRET_KEY, issuer=settings.TOKEN_ISS, algorithms=['HS256'])
    uid = payload.get('data', {}).get('uid', None)
    if not uid: return False
    cache = caches['access_token']
    server_token = cache.get(str(uid))
    if not server_token: return False
    if server_token != token: return False
    return uid


def refresh_access_token(token):
    """
    刷新token
    :param token: user request refresh_token
    :return payload/False: token data/verify lose
    """
    if not token: raise NotAuthenticated(detail='未携带身份信息')
    payload = jwt.decode(token, settings.SECRET_KEY, issuer=settings.TOKEN_ISS, algorithms=['HS256'])
    uid = payload.get('data', {}).get('uid', None)
    if not uid: return False
    refresh_cache = caches['refresh_token']
    access_cache = caches['access_token']
    server_token = refresh_cache.get(str(uid))
    if not server_token: return False
    if server_token != token: return False
    access_token = make_token(settings.ACCESS_TOKEN_OUT_TIME, uid)
    access_cache.set(str(uid), access_token, timeout=settings.ACCESS_TOKEN_OUT_TIME)
    return access_token


def remove_token(token):
    if not token: raise NotAuthenticated(detail='未携带身份信息')
    payload = jwt.decode(
        token,
        settings.SECRET_KEY,
        issuer=settings.TOKEN_ISS,
        algorithms=['HS256'],
        options={
            'verify_exp': False
        }
    )
    uid = payload.get('data', {}).get('uid', None)
    access_cache = caches['access_token']
    refresh_cache = caches['refresh_token']
    access_cache.delete(str(uid))
    refresh_cache.delete(str(uid))

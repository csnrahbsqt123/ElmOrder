import os

from redis import Redis


def url_base():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_redis_address():
    return Redis(host='127.0.0.1', port=6388)


class DevBase:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///{}/dev.db".format(url_base())
    SQLALCHEMY_TRACK_MODIFICATIONS = False


# 上线配置
class ProductBase(object):
    DEBUG = False


class DevConfig(DevBase):
    SESSION_TYPE = "redis"
    SESSION_REDIS = get_redis_address()

class DevAPIConfig(DevBase):
    SMS_LIFETIME = 300

    API_REDIS = get_redis_address()

    SECRET_KEY = 'elm_api'
    TOKEN_EXPIRES = 24 * 3600
    CART_LIFETIME = 3600

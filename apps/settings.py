import os

from redis import Redis


def url_base():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class DevBase:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///{}/dev.db".format(url_base())
    SQLALCHEMY_TRACK_MODIFICATIONS = False


# 上线配置
class ProductBase(object):
    DEBUG = False


class DevConfig(DevBase):
    SESSION_TYPE = "redis"
    SESSION_REDIS = Redis(host='192.168.199.132', port=6388)

class DevAPIConfig(DevBase):
    pass
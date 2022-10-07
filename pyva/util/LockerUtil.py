import time

from pyva.util.RedisUtil import RedisUtil


class LockerUtil:
    """
    Locker 基于redis的锁
    :version: 1.2
    :date: 2020-02-11
    """

    redis: RedisUtil

    def __init__(self, redis):
        self.redis = redis

    # 判断是否存在锁
    def hasLocked(self, key):
        return self.redis.getString('locker:' + key)

    # 加锁
    def lock(self, key, expiration=None):
        self.redis.setString('locker:' + key, str(time.time()), expiration)

    # 解锁
    def unlock(self, key):
        self.redis.delete('locker:' + key)

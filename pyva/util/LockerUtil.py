import time
from warnings import warn

from pyva.util.RedisUtil import RedisUtil


class LockerUtil:
    """
    Locker 基于redis的锁工具类

    作者：孙振强
    版本：2.0.1
    创建时间：2020-02-11
    修改时间：2023-11-21
    """

    PREFIX = 'locker:'
    redis: RedisUtil

    def __init__(self, redis: RedisUtil):
        self.redis = redis
        self.redis.initConn()

    def getFullKey(self, key: str) -> str:
        """
        获取完整的锁键名

        参数：
        - key: 锁键名

        返回值：
        - 完整的锁键名
        """
        return f'{self.PREFIX}:{key}'

    def isLocked(self, key: str):
        """
        判断是否存在锁

        参数：
        - key: 锁键名

        返回值：
        - 如果存在锁，返回锁的值；否则返回None
        """
        return self.redis.getString(self.getFullKey(key))

    def hasLocked(self, key: str):
        warn("请使用新方法：isLocked", DeprecationWarning)
        """
        判断是否存在锁（已废弃，请使用isLocked方法）

        参数：
        - key: 锁键名

        返回值：
        - 如果存在锁，返回锁的值；否则返回None
        """
        return self.isLocked(key)

    def lock(self, key: str, expiration=None):
        """
        加锁

        参数：
        - key: 锁键名
        - expiration: 锁的过期时间（可选）

        返回值：
        - True
        """
        self.redis.setString(self.getFullKey(key), str(time.time()), expiration)

        return True

    def unlock(self, key: str):
        """
        解锁

        参数：
        - key: 锁键名

        返回值：
        - True
        """
        if key.endswith("*"):
            keys = self.redis.conn.keys(self.getFullKey(key))

            if keys:
                for realKey in keys:
                    self.redis.delete(realKey)
        else:
            self.redis.delete(self.getFullKey(key))

        return True

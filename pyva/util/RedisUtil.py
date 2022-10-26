from redis import ConnectionPool, Redis

from pyva.config.RedisConfig import RedisConfig
from pyva.util.JsonUtil import JsonUtil


class RedisUtil:
    """
    RedisUtils redis工具类
    :version: 1.2
    :date: 2020-02-11
    """

    conn = None
    conn_pool = None
    config: RedisConfig = None

    def __init__(self, redisConfig: RedisConfig):
        self.config = redisConfig

        # self.conn = self.getConn(config)

        self.initConn()

    def initConn(self):
        if not self.conn:
            if not self.conn_pool:
                self.conn_pool = self.createPool(self.config)

            self.conn = Redis(connection_pool=self.conn_pool)

    @staticmethod
    def createPool(redisConfig: RedisConfig):
        return ConnectionPool(
            host=redisConfig.host,
            port=redisConfig.port,
            max_connections=redisConfig.maxConnections,
            username=redisConfig.username,
            password=redisConfig.password,
            db=redisConfig.database
        )

    @staticmethod
    def getConn(redisConfig: RedisConfig):
        return Redis(
            host=redisConfig.host,
            port=redisConfig.port,
            max_connections=redisConfig.maxConnections,
            username=redisConfig.username,
            password=redisConfig.password,
            db=redisConfig.database
        )

    def delete(self, key):
        self.initConn()
        return self.conn.delete(key)

    def setString(self, key, value, ex=None):
        self.initConn()
        return self.conn.set(key, value, ex)

    def getString(self, key):
        self.initConn()
        value = self.conn.get(key)

        if value:
            return str(value, "utf-8")
        else:
            return None

    def set(self, key, value, ex=None):
        self.initConn()
        return self.conn.set(key, JsonUtil.encode(value), ex)

    def get(self, key):
        self.initConn()
        value = self.conn.get(key)

        if value:
            return JsonUtil.decode(str(value, "utf-8"))
        else:
            return None

    def expire(self, key, ex=int):
        self.initConn()
        return self.conn.expire(key, ex)

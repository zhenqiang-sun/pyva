from pymongo import MongoClient
from pymongo.collection import Collection


class MongoConfig(object):
    """
    MongoConfig MongoDB配置类
    :version: 1.1
    :date: 2020-02-12
    """

    host = 'mongodb'
    port = 27017
    username = 'root'
    password = ''
    database = ''
    authDatabase = ''

    def getUrl(self):
        config = [
            'mongodb://',
            self.username,
            ':',
            self.password,
            '@',
            self.host,
            ':',
            str(self.port),
            '/',
            self.database,
            '?authSource=',
            self.authDatabase,
            '&authMechanism=SCRAM-SHA-256',
        ]

        return ''.join(config)


class MongoUtil(object):
    """
    MongoUtils MongoDB工具类
    :version: 1.1
    :date: 2020-02-12
    """

    config: MongoConfig = None
    defaultConfig: MongoConfig = None

    def __init__(self, config: MongoConfig = None):
        if config:
            self.config = config
        else:
            self.config = self.defaultConfig

    def getClient(self):
        """
        返回Mongo数据库连接，同步
        :return:
        """
        try:
            client = MongoClient(self.config.getUrl())
            return client
        except Exception as e:
            raise str(e)

    def getDb(self):
        """
        返回Mongo数据库实例
        :param database:
        :return:
        """

        try:
            client = self.getClient()
            db = client[self.config.database]
            return db
        except Exception as e:
            raise str(e)

    def getCollection(self, collection_name):
        """
        返回输入的名称对应的集合
        :param collection_name:
        :return:
        """

        try:
            db = self.getDb()
            collection: Collection = db[collection_name]
            return collection
        except Exception as e:
            raise str(e)

class MongoConfig:
    """
    MongoConfig MongoDB配置类

    :version: 1.1
    :date: 2020-02-12
    """

    host: str = "mongodb"
    port: int = 27017
    username = "root"
    password: str = ""
    database: str = ""

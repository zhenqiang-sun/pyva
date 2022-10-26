class RedisConfig:
    """
    pyva RedisConfig Redis配置类

    :version: 1.3
    :createdDate: 2020-02-11
    :updatedDate: 2022-10-03
    """

    # 主机
    host: str = "localhost"
    # 端口
    port: int = 6379
    # 账号
    username: str = "root"
    # 密码
    password: str = None
    # 数据库
    database: int = 0
    # 最大连接数
    maxConnections: int = 100

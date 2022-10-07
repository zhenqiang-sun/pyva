class DbConfig(object):
    """
    pyva DbConfig DB配置类
    :version: 1.5
    :createdDate: 2020-02-11
    :updatedDate: 2022-10-03
    """

    # 驱动，默认mysql
    driver: str = "mysql+pymysql"
    # 主机
    host: str = "localhost"
    # 端口
    port: int = 3306
    # 账号
    username: str = "root"
    # 密码
    password: str = ""
    # 数据库
    database: str = ""
    # 字符集
    charset: str = "utf8mb4"
    # 表前缀
    prefix: str = ""
    # 是否输出
    echo: bool = True
    # 连接池大小
    poolSize: int = 100
    # 最大连接
    maxOverflow: int = 100
    # 回收时间
    poolRecycle: int = 60
    # 自动flush
    autoFlush: bool = True
    # 自动提交
    autoCommit: bool = True
    # 过期提交
    expireOnCommit: bool = False

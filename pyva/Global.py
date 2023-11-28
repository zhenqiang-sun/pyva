import logging
import os

from sqlalchemy.orm import Session

from pyva.util import MongoUtil
from pyva.util.LockerUtil import LockerUtil
from pyva.util.NacosUtil import NacosUtil
from pyva.util.RedisUtil import RedisUtil


class G:
    # 运行模式：是否Debug模式
    debug: bool = False
    # 运行环境
    env: str = None
    # 运行目录
    path: str = None
    # 静态资源路径
    staticPath: str = None
    # 临时文件路径
    temporaryPath: str = None
    # 静态资源路径
    resPath: str = None
    # 静态资源路径
    sqlPath: str = None
    # 日志输出
    logger = logging.getLogger('pyva')
    # 全局nacos
    nacos: NacosUtil = None
    # 全局db的sess
    db: Session = None
    # 全局redis
    redis: RedisUtil = None
    # 全局redis
    mongo: MongoUtil = None
    # 全局locker
    locker: LockerUtil = None
    # 是否初始化
    isInitialized: bool = False

    @staticmethod
    def init(AppConfig):
        if G.isInitialized:
            return False

        from pyva.util.ConfigUtil import ConfigUtil
        ConfigUtil.initConfigForStartup(AppConfig)

        # 运行模式：是否Debug模式
        G.debug = AppConfig.debug
        # 运行环境
        G.env = AppConfig.env
        # 运行目录
        G.path = AppConfig.srcPath
        # SQL文件路径
        G.sqlPath = G.path + os.sep + "sql"
        # 静态文件路径
        G.staticPath = G.path + os.sep + "static"
        # 模板文件路径
        G.templatesPath = G.path + os.sep + "templates"
        # 临时文件路径
        G.temporaryPath = G.path + os.sep + "temporary"
        # 静态资源路径
        G.resPath = AppConfig.rootPath + os.sep + "res"

        return True

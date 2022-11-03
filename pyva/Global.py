import logging

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

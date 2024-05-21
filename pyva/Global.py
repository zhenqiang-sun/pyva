import logging

from sqlalchemy.orm import Session


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
    nacos = None
    # 全局db的sess
    db: Session = None
    # 全局redis
    redis = None
    # 全局redis
    mongo = None
    # 全局locker
    locker = None
    # 是否初始化
    isInitialized: bool = False

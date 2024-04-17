import os

from pyva.Global import G
from pyva.common.LoggerHandler import LoggingHandler


def GlobalInit(AppConfig):
    G.logger.info("GlobalInit")

    if G.isInitialized:
        G.logger.info("GlobalInit-isInitialized")
        return False

    from pyva.util.ConfigUtil import ConfigUtil
    ConfigUtil.initConfigForGlobal(AppConfig)

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

    # 配置日志处理器
    G.logger.addHandler(LoggingHandler())

    # G初始化完成
    G.isInitialized = True

    return True

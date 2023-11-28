import os

from pyva.Global import G
from pyva.common.LoggerHandler import LoggingHandler


def GlobalInit(AppConfig):
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

    G.logger.addHandler(LoggingHandler())

    return True

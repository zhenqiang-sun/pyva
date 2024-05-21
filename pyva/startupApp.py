import sys

import uvicorn

from pyva.Global import G
from pyva.util.ConfigUtil import ConfigUtil


# 运行项目
def initUvicornConfig(AppConfig):
    G.logger.info("initUvicornConfig")
    ConfigUtil.initConfigForStartup(AppConfig)
    LoggingConfig = ConfigUtil.importConfig(AppConfig.srcPath, "logging")

    if "debug" in sys.argv:
        AppConfig.debug = True

    uvicornConfig = {
        "app": "src.Application:App",
        "host": "0.0.0.0",
        "port": AppConfig.port,
        "log_config": LoggingConfig,
        "workers": AppConfig.workers,
    }

    if AppConfig.debug:
        uvicornConfig["workers"] = 1
        uvicornConfig["reload"] = True
        uvicornConfig["reload_dirs"] = [AppConfig.srcPath]

    if AppConfig.https:
        uvicornConfig["ssl_keyfile"] = AppConfig.srcPath + "/template/cert.key"
        uvicornConfig["ssl_certfile"] = AppConfig.srcPath + "/template/cert_public.crt"

    return uvicornConfig


def runUvicorn(uvicornConfig):
    G.logger.info("runUvicorn")
    uvicorn.run(**uvicornConfig)

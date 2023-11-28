import uvicorn

from pyva.util.ConfigUtil import ConfigUtil


# 运行项目
def initUvicornConfig(AppConfig, LoggingConfig, debug):
    ConfigUtil.initConfigForStartup(AppConfig)

    if debug:
        AppConfig.debug = debug

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

    return uvicornConfig


def runUvicorn(uvicornConfig):
    uvicorn.run(**uvicornConfig)

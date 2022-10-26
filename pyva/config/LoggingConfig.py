class LoggingLevel:
    """
    日志基本：CRITICAL > ERROR > WARNING > INFO > DEBUG
    """
    CRITICAL: str = "CRITICAL"
    ERROR: str = "ERROR"
    WARNING: str = "WARNING"
    INFO: str = "INFO"
    DEBUG: str = "DEBUG"


def generateLoggingConfig(loggingPath: str, loggingLevel: str):
    """
    生成日志配置

    :version: 1.0.2
    :createdDate: 2022-10-01
    :updatedDate: 2022-10-03
    """

    loggingConfig: dict = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(asctime)s | %(levelname)s | %(name)s | %(filename)s:%(lineno)d -> %(module)s.%(funcName)s | %(message)s"
            },
            "simple": {
                "format": "%(asctime)s | %(levelname)s %(message)s"
            }
        },
        "handlers": {
            "console": {
                "level": loggingLevel,
                "class": "logging.StreamHandler",
                "formatter": "standard",
                "stream": "ext://sys.stdout"
            },
            "file_error": {
                "level": "ERROR",
                "class": "logging.handlers.TimedRotatingFileHandler",
                "filename": loggingPath + "pyva_error.log",
                "when": "MIDNIGHT",
                "backupCount": 100,
                "formatter": "standard",
                "encoding": "utf-8",
                "delay": True
            },
            "file_info": {
                "level": "INFO",
                "class": "logging.handlers.TimedRotatingFileHandler",
                "filename": loggingPath + "pyva_info.log",
                "when": "MIDNIGHT",
                "backupCount": 10,
                "formatter": "standard",
                "encoding": "utf-8",
                "delay": True
            },
            "file_debug": {
                "level": "DEBUG",
                "class": "logging.handlers.TimedRotatingFileHandler",
                "filename": loggingPath + "pyva_debug.log",
                "when": "MIDNIGHT",
                "backupCount": 3,
                "formatter": "standard",
                "encoding": "utf-8",
                "delay": True
            }
        },
        "loggers": {
            "fastapi": {
                "level": "DEBUG"
            },
            "nacos.client": {
                "level": "ERROR"
            },
            "tortoise": {
                "level": "DEBUG"
            },
            "uvicorn": {
                "level": "DEBUG"
            },
            "uvicorn.error": {
                "level": "INFO",
                "propagate": False
            },
            "uvicorn.access": {
                "level": "INFO",
                # "propagate": False
            },
            "asyncio": {
                "level": "ERROR"
            },
            "watchfiles": {
                "level": "ERROR"
            },
            "urllib3": {
                "level": "ERROR"
            }
        },
        "root": {
            "level": loggingLevel,
            "handlers": [
                "console",
                "file_error",
                # "file_info",
                # "file_debug"
            ]
        }
    }

    if loggingLevel == "INFO":
        loggingConfig["root"]["handlers"].append("file_info")

    if loggingLevel == "DEBUG":
        loggingConfig["root"]["handlers"].append("file_debug")

    return loggingConfig


LoggingConfig = generateLoggingConfig("../logs/", LoggingLevel.DEBUG)

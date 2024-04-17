from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError, HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from pyva.Global import G
from pyva.common.FastapiEvents import FastapiEvents
from pyva.common.FastapiException import FastapiException


def initAppOnly(FastapiConfig):
    # 实例化：FastAPI
    App = FastAPI(**FastapiConfig.__dict__)
    return App


def initAppBase(FastapiConfig):
    G.logger.info("initAppBase")
    App = initAppOnly(FastapiConfig)
    # 异常错误处理
    App.add_exception_handler(RequestValidationError, FastapiException.validationError)
    App.exception_handler(HTTPException)(FastapiException.http_exception_handler)
    App.exception_handler(Exception)(FastapiException.generic_exception_handler)

    if FastapiConfig.allowCors:
        # 注册CORS
        App.add_middleware(
            CORSMiddleware,
            allow_origins=FastapiConfig.corsOrigins,
            allow_credentials=True,
            allow_methods=['*'],
            allow_headers=['*'],
        )

    # 注册：启动事件
    App.add_event_handler('startup', FastapiEvents.startup)
    # 注册：停止事件
    App.add_event_handler('shutdown', FastapiEvents.shutdown)

    # 注册：静态资源目录
    App.mount("/static", StaticFiles(directory=G.staticPath))
    App.mount("/res", StaticFiles(directory=G.resPath))

    return App

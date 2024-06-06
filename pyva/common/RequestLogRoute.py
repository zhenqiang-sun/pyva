import _thread
import traceback
from typing import Callable

from fastapi.exceptions import RequestValidationError, ResponseValidationError
from fastapi.routing import APIRoute
from starlette import status
from starlette.requests import Request
from starlette.responses import Response

from pyva.Global import G
from pyva.entity.RequestLog import RequestLog
from pyva.service.RequestLogService import RequestLogService
from pyva.util.JsonUtil import JsonUtil


class RequestLogRoute(APIRoute):
    """
    自定义APIRoute，用于记录RequestLog
    """

    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            # 创建：requestLog
            requestLog: RequestLog = await RequestLogService.createRequestLog(request)
            response = None
            responseBody = None
            responseError = None

            try:
                response: Response = await original_route_handler(request)
            except RequestValidationError as exc:
                responseBody = {
                    'code': status.HTTP_400_BAD_REQUEST,
                    'message': 'Bad Request',
                }

                # responseError = str(exc)
                responseError = self.getExceptionTracebackDetail(exc)
                G.logger.warning(f"ResponseValidationError: {responseError}")
            except ResponseValidationError as exc:
                responseBody = {
                    'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'message': 'Bad Response',
                }

                # responseError = str(exc)
                responseError = self.getExceptionTracebackDetail(exc)
                G.logger.error(f"ResponseValidationError: {responseError}")
            except Exception as exc:
                if hasattr(exc, 'status_code') and hasattr(exc, 'detail'):
                    responseBody = {
                        'code': exc.status_code,
                        'message': 'Exception',
                    }

                    if exc.status_code == status.HTTP_401_UNAUTHORIZED:
                        responseBody["message"] = exc.detail

                else:
                    responseBody = {
                        'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                        'message': 'Exception',
                    }

                if responseBody["message"] == 'Exception':
                    responseError = self.getExceptionTracebackDetail(exc)
                    G.logger.error(f"Exception: {responseError} ")

            if responseBody:
                response = Response(status_code=responseBody.get("code"), content=JsonUtil.encode(responseBody), media_type="application/json", )
                response.error = responseError

            # 设置：response中设置requestId
            response.headers["X-Request-Id"] = requestLog.requestId

            # 更新：异步保存requestLog
            _thread.start_new_thread(RequestLogService.updateRequestLog, (request, response,))

            return response

        return custom_route_handler

    @staticmethod
    def getExceptionTracebackDetail(exc):
        # 获取异常的堆栈跟踪信息
        tb = exc.__traceback__
        detail = ''.join(traceback.format_exception(None, exc, tb))

        return detail

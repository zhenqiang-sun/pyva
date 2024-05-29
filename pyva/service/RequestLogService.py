from starlette.requests import Request
from starlette.responses import Response
from ulid import Monotonic

from pyva.Global import G
from pyva.common.RequestLogStatusEnum import RequestLogStatusEnum
from pyva.common.RequestLogTypeEnum import RequestLogTypeEnum
from pyva.config.AppConfig import AppConfig
from pyva.entity.RequestLog import RequestLog
from pyva.util.JsonUtil import JsonUtil
from pyva.util.TimeUtil import TimeUtil


class RequestLogService():

    @classmethod
    async def createRequestLog(cls, request: Request):
        # 构造请求日志
        requestLog = RequestLog()

        if request.headers.get("X-Request-Id"):
            requestLog.id = request.headers.get("X-Request-Id")
        else:
            requestLog.id = Monotonic().generate()

        requestLog.createdTime = TimeUtil.getNow()
        requestLog.updatedTime = requestLog.createdTime
        requestLog.type = RequestLogTypeEnum.外部请求.value
        requestLog.status = RequestLogStatusEnum.请求中.value
        requestLog.serviceId = AppConfig.id
        requestLog.serviceName = AppConfig.name
        requestLog.requestId = requestLog.id
        requestLog.requestTimestamp = TimeUtil.getTimestampUseMillisecond()
        requestLog.requestTime = requestLog.createdTime
        requestLog.requestIp = request.client.host

        if request.headers.get("X-Real-Ip"):
            requestLog.requestIp = request.headers.get("X-Real-Ip")
        elif request.headers.get("Remote-Host"):
            requestLog.requestIp = request.headers.get("Remote-Host")
        else:
            requestLog.requestIp = request.client.host

        requestLog.requestPort = request.url.port
        requestLog.requestUrl = str(request.url)
        requestLog.requestMethod = request.method
        requestLog.requestScheme = request.url.scheme
        requestLog.requestPath = request.url.path
        requestLog.requestParams = dict(request.query_params)
        requestLog.requestHeaders = dict(request.headers)
        requestLog.requestHeaders.pop("cookie", None)
        requestLog.requestCookies = dict(request.cookies)
        requestLog.requestUseragent = request.headers.get("User-Agent")

        requestContentType = request.headers.get("Content-Type")

        if not requestContentType or requestContentType == "application/octet-stream" or requestContentType.startswith("multipart/form-data"):
            pass
        elif request.headers.get("Content-Type") == "application/json":
            try:
                requestLog.requestJson = await request.json()
            except:
                pass
        elif request.headers.get("Content-Type") == "application/x-www-form-urlencoded":
            try:
                requestLog.requestJson = dict(await request.form())
            except:
                pass
        else:
            try:
                requestLog.requestBody = await request.body()
            except:
                pass

        request.state.requestLog = requestLog

        return requestLog

    @classmethod
    def updateRequestLog(cls, request: Request, response: Response):
        # 判断：requestLog是否存在
        if not hasattr(request.state, "requestLog"):
            return

        # 提取: requestLog
        requestLog = request.state.requestLog

        # 补充请求日志
        requestLog.updatedTime = TimeUtil.getNow()
        requestLog.status = RequestLogStatusEnum.已返回.value
        requestLog.responseTimestamp = TimeUtil.getTimestampUseMillisecond()
        requestLog.responseTime = requestLog.updatedTime
        requestLog.responseUseTime = requestLog.responseTimestamp - requestLog.requestTimestamp
        requestLog.responseIp = G.ip
        requestLog.responseCode = response.status_code
        requestLog.responseHeaders = dict(response.headers)

        # 提取：responseBody
        responseContentType = response.headers.get("Content-Type")

        try:
            if responseContentType == "application/json":
                requestLog.responseJson = JsonUtil.decode(response.body)
            elif responseContentType == "text/plain":
                requestLog.responseBody = response.body
        except:
            pass

        # 判断：responseCode
        if response.status_code >= 400:
            requestLog.status = RequestLogStatusEnum.有异常.value

            if hasattr(response, "error"):
                requestLog.responseError = response.error
        else:
            requestLog.status = RequestLogStatusEnum.已成功.value

        # 保存入库
        G.db.add(requestLog)
        G.db.commit()

import traceback
from typing import Union

from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from pyva.Global import G
from pyva.dto.BaseDto import RespDataDto


class FastapiException:

    @staticmethod
    async def validationError(_: Request, exc: Union[RequestValidationError, ValidationError], ) -> JSONResponse:
        """    参数校验错误处理    """
        G.logger.error(f"参数校验错误处理: {exc.errors()=}")

        resp = RespDataDto(code=422, message="数据校验错误")

        if G.debug:
            resp.data = exc.errors()

        return JSONResponse(resp.dict(by_alias=True), status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

    @staticmethod
    async def http_exception_handler(request, exc):
        await FastapiException.report_exception(request, exc)

        return JSONResponse(
            status_code=exc.status_code,
            content={
                "code": exc.status_code,
                "message": exc.detail
            },
        )

    @staticmethod
    async def generic_exception_handler(request, exc):
        await FastapiException.report_exception(request, exc)

        return JSONResponse(
            status_code=500,
            content={
                "code": 500,
                "message": "Internal Server Error"
            },
        )

    @staticmethod
    async def report_exception(request, exc):
        # 4xx错误不上报
        if hasattr(exc, "status_code") and str(exc.status_code).startswith("4"):
            return

        # 组装异常信息
        msg = f"""
request_method: {request.method}
request_url: {request.url}
exception: {exc}
traceback: {''.join(traceback.format_exception(exc))}
        """

        # 上报异常
        G.logger.error(msg)

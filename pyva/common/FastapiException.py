import traceback
from typing import Union

from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from pyva.Global import G
from pyva.dto.BaseDto import RespDataDto
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.config.FastapiConfig import FastapiConfig


class FastapiException:

    @staticmethod
    async def validationError(_: Request, exc: Union[RequestValidationError, ValidationError], ) -> JSONResponse:
        """    参数校验错误处理    """
        G.logger.error(f"参数校验错误处理: {exc.errors()=}")

        resp = RespDataDto(code=422, message="数据校验错误")

        if FastapiConfig.debug:
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
        msg = f"request_method:{request.method}\n"
        msg += f"request_url:{request.url}\n"
        msg += f"exception:{exc}\n"
        msg += "traceback:" + "".join(traceback.format_exception(exc))

        G.logger.error(msg)

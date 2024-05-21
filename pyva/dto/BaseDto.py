from typing import List, Dict, TypeVar

from pydantic import BaseModel, Field

from pyva.util.JsonUtil import JsonUtil

DataT = TypeVar("DataT")


class BaseDto(BaseModel):
    """
    基础DTO
    """

    class Config:
        json_encoders = JsonUtil.jsonEncoders  # 使用自定义json转换


class BaseEntityDto(BaseModel):
    """
    基础Entity DTO
    """

    class Config:
        json_encoders = JsonUtil.jsonEncoders
        from_attributes = True  # 为模型实例


class RespDto(BaseDto):
    """
    基础返回DTO
    """
    code: int = Field(..., gt=0, description='返回码')
    message: str = Field(..., description='返回说明')


class SuccessRespDto(RespDto):
    """
    成功响应DTO
    """
    code: int = 10000
    message: str = "SUCCESS"


class FailRespDto(RespDto):
    """
    失败响应DTO
    """
    code: int = 19999
    message: str = "FAIL"


class RespIdDto(SuccessRespDto):
    """
    ID返回DTO
    """
    id: int | str = Field(..., gt=0, description='数据ID')


class RespDataDto(SuccessRespDto):
    """
    Data返回DTO
    """
    data: dict = None  # 返回Data


class RespDetailDto(SuccessRespDto):
    """
    详情返回DTO
    """
    detail: dict = None  # 返回详情


class RespListDto(SuccessRespDto):
    """
    列表返回DTO
    """
    list: List[Dict] = None  # 数据list

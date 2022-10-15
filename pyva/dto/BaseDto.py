from typing import List, Dict

from pydantic import BaseModel

from pyva.util.JsonUtil import JsonUtil


class BaseDto(BaseModel):
    """
    基础DTO
    """

    class Config:
        json_encoders = JsonUtil.jsonEncoders  # 使用自定义json转换


class BaseEntitySchema(BaseModel):
    """
    基础Entity DTO
    """

    class Config:
        json_encoders = JsonUtil.jsonEncoders
        orm_mode = True  # 为模型实例


class RespDto(BaseDto):
    """
    基础返回DTO
    """
    code: int = 0  # 返回编号
    message: str = ""  # 返回消息


class RespIdDto(RespDto):
    """
    ID返回DTO
    """
    id: int = 0  # 返回id


class RespDataDto(RespDto):
    """
    Data返回DTO
    """
    data: dict = None  # 返回Data


class RespSuccessDto(RespDataDto):
    """
    成功返回DTO
    """
    code = 10000
    message = "SUCCESS"


class RespErrorDto(RespDataDto):
    """
    成功返回DTO
    """
    code = 19999
    message = "FAIL"


class RespDetailDto(RespDto):
    """
    详情返回DTO
    """
    detail: dict = None  # 返回详情


class RespListDto(RespDto):
    """
    列表返回DTO
    """
    list: List[Dict] = None  # 数据list


class RespPageDto(RespDto):
    """
    列表返回DTO
    """
    page: int = 0  # 当前页码
    size: int = 0  # 每页大小
    count: int = 0  # 数据总条数
    pageCount: int = 0  # 总页数
    list: List[Dict] = None  # 数据list

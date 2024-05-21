from typing import List

from pydantic import BaseModel

from pyva.dto.BaseDto import BaseEntityDto, DataT


class ListFilterDto(BaseModel):
    """
    列表参数：过滤条件Schema
    """
    key: str  # 字段名
    condition: str  # 条件
    value: DataT  # 条件值，如condition为in或!in时，value为用“,”分割的多值得字符串


class ListOrderDto(BaseModel):
    """
    列表参数：排序条件Schema
    """
    key: str  # 字段名
    condition: str  # 排序条件


class ListKeyDto(BaseModel):
    """
    列表参数：字段条件Schema
    """
    key: str  # 字段名
    rename: str = None  # 字段名重命名, 为空则不进行重命名


class ListReqDto(BaseModel):
    """
    列表参数Schema
    """
    page: int = 1  # 当前页码
    size: int = 10  # 每页条数
    keywords: str = None  # 关键字，用于模糊、分词搜索
    deleted: str = None
    userId: int | str = None  # 数据对应用户id
    filters: List[ListFilterDto] = None  # 过滤条件
    orders: List[ListOrderDto] = None  # 排序条件
    keys: List[ListKeyDto] = None  # 字段条件


class ListPageDto(BaseModel):
    """
    列表返回DTO
    """
    page: int = 0  # 当前页码
    size: int = 0  # 每页大小
    count: int = 0  # 数据总条数
    pageCount: int = 0  # 总页数
    list: List[BaseEntityDto] = None  # 数据list

from enum import Enum, unique


@unique
class OrderConditionEnum(Enum):
    """
    排序条件枚举
    """

    asc = "asc"
    desc = "desc"
    rand = "rand"

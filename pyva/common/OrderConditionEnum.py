from enum import Enum, unique


@unique
class OrderConditionEnum(Enum):
    """
    排序条件枚举
    """

    acs = "acs"
    desc = "desc"
    rand = "rand"

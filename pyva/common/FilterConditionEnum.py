from enum import Enum, unique


@unique
class FilterConditionEnum(Enum):
    """
    过滤条件枚举
    """

    eq = "="
    gt = ">"
    lt = "<"
    gte = ">="
    lte = "<="
    ne = "!="
    like = "like"
    in_ = "in"
    not_in = "!in"
    is_null = "null"
    not_null = "!null"

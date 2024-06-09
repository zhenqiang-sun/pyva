from enum import Enum, unique


@unique
class FilterConditionEnum(Enum):
    """
    过滤条件枚举
    """

    EQ = "="
    GT = ">"
    LT = "<"
    GTE = ">="
    LTE = "<="
    NE = "!="
    LIKE = "like"
    IN = "in"
    NOT_IN = "!in"
    IS_NULL = "null"
    NOT_NULL = "!null"

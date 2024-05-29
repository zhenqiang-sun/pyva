from enum import Enum, unique


@unique
class RequestLogStatusEnum(Enum):
    请求中 = 1
    已返回 = 2
    已成功 = 3
    有异常 = 4

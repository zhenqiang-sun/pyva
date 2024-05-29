from enum import Enum, unique


@unique
class RequestLogTypeEnum(Enum):
    外部请求 = 1
    内部调用 = 2
    请求外部 = 3

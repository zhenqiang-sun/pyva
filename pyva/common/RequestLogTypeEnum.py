from enum import Enum, unique


@unique
class RequestLogTypeEnum(Enum):
    EXTERNAL_REQUEST = 1  # 外部请求
    INTERNAL_CALL = 2  # 内部调用
    REQUEST_EXTERNAL = 3  # 请求外部

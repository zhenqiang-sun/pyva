from enum import Enum, unique


@unique
class RequestLogStatusEnum(Enum):
    PENDING = 0  # 待处理
    REQUESTING = 1  # 请求中
    RETURNED = 2  # 已返回
    SUCCESSFUL = 3  # 已成功
    EXCEPTION = 4  # 有异常
    FAILED = 5  # 处理失败

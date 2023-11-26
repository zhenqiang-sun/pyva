import datetime
import decimal

import orjson


class JsonUtil:
    """
    JSON工具类

    作者：孙振强
    版本：2.0.1
    创建时间：2022-10-07
    修改时间：2023-11-21
    """

    # 定义JSONEncoders
    jsonEncoders = {
        # 解决日期和时间中“T”字符的格式问题
        datetime.datetime: lambda dt: dt.isoformat(" "),
        decimal.Decimal: lambda dt: str(dt),
    }

    def default(obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        raise TypeError

    @staticmethod
    def encode(obj):
        return orjson.dumps(obj, default=JsonUtil.default).decode("utf-8")

    @staticmethod
    def decode(s):
        return orjson.loads(s)

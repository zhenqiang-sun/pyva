import datetime
import decimal

import orjson


class JsonUtil:
    """
    定义JSONEncoders
    """
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

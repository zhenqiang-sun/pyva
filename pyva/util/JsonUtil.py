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
        # decimal.Decimal: lambda dt: str(dt),
    }

    @staticmethod
    def encode(obj):
        return orjson.dumps(obj).decode("utf-8")

    @staticmethod
    def decode(s):
        return orjson.loads(s)

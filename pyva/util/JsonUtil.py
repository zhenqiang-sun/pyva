import datetime
import decimal
import json


class JsonUtil:
    """
    定义JSONEncoders
    """
    jsonEncoders = {
        # 解决日期和时间中“T”字符的格式问题
        datetime.datetime: lambda dt: dt.isoformat(" "),
        datetime.date: lambda dt: dt.isoformat(" "),
        decimal.Decimal: lambda dt: str(dt),
    }

    @staticmethod
    def encode(obj):
        json.dumps(obj, ensure_ascii=False)

    @staticmethod
    def decode(s):
        json.loads(s)

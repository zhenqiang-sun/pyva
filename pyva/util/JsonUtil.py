import datetime
import decimal


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

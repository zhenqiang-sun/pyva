import time
from datetime import datetime
from time import struct_time
from warnings import warn


class TimeUtil:
    """
    时间（日期）工具类，提供了一些常用的时间、日期操作方法

    作者：孙振强
    版本：2.0.1
    修改时间：2023-11-21
    """

    # 定义：时间格式
    TIME_FORMAT = "%H:%M:%S"
    # 定义：日期格式
    DATE_FORMAT = "%Y-%m-%d"
    # 定义：日期时间格式
    DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

    def __init__(self):
        pass

    @staticmethod
    def format(timeObj: struct_time, timeFormat: str) -> str:
        """
        将时间对象格式化为指定格式的字符串

        参数：
        - timeObj：时间对象
        - timeFormat：时间格式

        返回值：
        - 格式化后的时间字符串
        """
        return time.strftime(timeFormat, timeObj)

    @staticmethod
    def formatTime(timeObj: struct_time, timeFormat: str = TIME_FORMAT) -> str:
        """
        将时间对象格式化为时间字符串
        """
        return TimeUtil.format(timeObj, timeFormat)

    @staticmethod
    def getFormatTime(timeObj):
        warn("请使用新方法：formatTime", DeprecationWarning)
        return TimeUtil.formatTime(timeObj)

    @staticmethod
    def formatDate(timeObj: struct_time, timeFormat: str = DATE_FORMAT) -> str:
        """
        将时间对象格式化为日期字符串
        """
        return TimeUtil.format(timeObj, timeFormat)

    @staticmethod
    def getFormatDate(timeObj):
        warn("请使用新方法：formatDate", DeprecationWarning)
        return TimeUtil.formatDate(timeObj)

    @staticmethod
    def formatDatetime(timeObj: struct_time, timeFormat: str = DATETIME_FORMAT) -> str:
        """
        将时间对象格式化为日期时间字符串
        """
        return TimeUtil.format(timeObj, timeFormat)

    @staticmethod
    def getFormatDatetime(timeObj):
        warn("请使用新方法：formatDatetime", DeprecationWarning)
        return TimeUtil.formatDatetime(timeObj)

    @staticmethod
    def getTimeObjByTimestamp(timestamp: int) -> struct_time:
        """
        将时间戳转换为本地时间

        参数：
        - timestamp：时间戳

        返回值：
        - 本地时间对象
        """
        return time.localtime(timestamp)

    @staticmethod
    def getLocalTime(timestamp):
        warn("请使用新方法：getTimeObj", DeprecationWarning)
        return TimeUtil.getTimeObjByTimestamp(timestamp)

    @staticmethod
    def getTimeObjNow() -> struct_time:
        """
        获取当前时间对象
        """
        return time.localtime()

    @staticmethod
    def getNow():
        return TimeUtil.getTimeObjNow()

    @staticmethod
    def getTimeObjByTimeStr(timeStr: str, timeFormat: str = DATETIME_FORMAT) -> struct_time:
        """
        将指定格式的时间字符串转换为时间对象

        参数：
        - timeStr：时间字符串
        - timeFormat：时间格式

        返回值：
        - 时间对象
        """
        timeStr = str(timeStr).replace("T", " ")
        return time.strptime(timeStr, timeFormat)

    @staticmethod
    def getTimeStrNow(timeFormat: str = TIME_FORMAT) -> str:
        """
        获取当前时间指定格式的时间字符串
        """
        return TimeUtil.format(TimeUtil.getTimeObjNow(), timeFormat)

    @staticmethod
    def getDateStrNow(timeFormat: str = DATE_FORMAT) -> str:
        """
        获取当前时间指定格式的日期字符串
        """
        return TimeUtil.format(TimeUtil.getTimeObjNow(), timeFormat)

    @staticmethod
    def getDate():
        warn("请使用新方法：getDateStrNow", DeprecationWarning)
        return TimeUtil.getDateStrNow()

    @staticmethod
    def getDatetimeStrNow(timeFormat: str = DATETIME_FORMAT) -> str:
        """
        获取当前时间指定格式的日期时间字符串
        """
        return TimeUtil.format(TimeUtil.getTimeObjNow(), timeFormat)

    @staticmethod
    def getNowUesFormat():
        warn("请使用新方法：getDatetimeStrNow", DeprecationWarning)
        return TimeUtil.getTimeStrNow()

    @staticmethod
    def getTimestamp() -> int:
        """
        获取当前时间的时间戳（分级）
        """
        return int(round(time.time()))

    @staticmethod
    def getTimestampUseSecond():
        warn("请使用新方法：getTimestamp", DeprecationWarning)
        return TimeUtil.getTimestamp()

    @staticmethod
    def getTimestampUseMillisecond() -> int:
        """
        获取当前时间的时间戳（毫秒级）
        """
        return int(round(time.time() * 1000))

    @staticmethod
    def formatTimestamp(timestamp: int, timeFormat: str = DATETIME_FORMAT):
        """
        将时间戳转换为指定格式的时间字符串（时:分:秒）
        """
        return TimeUtil.format(TimeUtil.getTimeObjByTimestamp(timestamp), timeFormat)

    @staticmethod
    def getFormatDatetimeFromTimestamp(timestamp):
        warn("请使用新方法：formatTimestamp", DeprecationWarning)
        return TimeUtil.formatTimestamp(timestamp)

    @staticmethod
    def getTimeObjFormFormatDatetime(timeStr):
        warn("请使用新方法：getTimeObjByTimeStr", DeprecationWarning)
        return TimeUtil.getTimeObjByTimeStr(timeStr)

    @staticmethod
    def getTimestampByTimeObj(timeObj: time) -> int:
        """
        将指定格式的时间字符串转换为时间戳
        """
        return int(time.mktime(timeObj))

    @staticmethod
    def getTimestampByTimeStr(timeStr: str, timeFormat: str = DATETIME_FORMAT) -> int:
        """
        将指定格式的时间字符串转换为时间戳
        """
        return TimeUtil.getTimestampByTimeObj(TimeUtil.getTimeObjByTimeStr(timeStr, timeFormat))

    @staticmethod
    def getTimestampFormFormatDatetime(timeStr):
        warn("请使用新方法：getTimestampByTimeStr", DeprecationWarning)
        return TimeUtil.getTimestampByTimeStr(timeStr)

    @staticmethod
    def calculateDaysBetween(startTimeStr, endTimeStr, timeFormat=DATE_FORMAT) -> int:
        """
        计算两个时间之间的天数差

        参数：
        - startTimeStr：起始时间
        - endTimeStr：结束时间

        返回值：
        - 两个时间之间的天数差
        """

        startObj = datetime.strptime(startTimeStr, timeFormat)
        endObj = datetime.strptime(endTimeStr, timeFormat)

        daysDiff = (endObj - startObj).days

        return daysDiff

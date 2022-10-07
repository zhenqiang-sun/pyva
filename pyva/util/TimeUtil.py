import time


class TimeUtil:

    @staticmethod
    def getFormatDatetime(timeObj):
        return time.strftime("%Y-%m-%d %H:%M:%S", timeObj)

    @staticmethod
    def getFormatDate(timeObj):
        return time.strftime("%Y-%m-%d", timeObj)

    @staticmethod
    def getFormatTime(timeObj):
        return time.strftime("%H:%M:%S", timeObj)

    @staticmethod
    def getLocalTime(timestamp):
        return time.localtime(timestamp)

    @staticmethod
    def getNow():
        return TimeUtil.getLocalTime(time.time())

    @staticmethod
    def getNowUesFormat():
        return time.strftime("%Y-%m-%d %H:%M:%S", TimeUtil.getNow())

    @staticmethod
    def getDate():
        return time.strftime("%Y-%m-%d", TimeUtil.getNow())

    @staticmethod
    def getTimestampUseSecond():
        return int(round(time.time()))

    @staticmethod
    def getTimestampUseMillisecond():
        return int(round(time.time() * 1000))

import time
import unittest
from datetime import datetime

from pyva.util.TimeUtil import TimeUtil


class TimeUtilTest(unittest.TestCase):

    def test_format(self):
        timeObj = datetime.now().timetuple()
        timeFormat = "%Y-%m-%d %H:%M:%S"
        expected = datetime.now().strftime(timeFormat)
        self.assertEqual(TimeUtil.format(timeObj, timeFormat), expected)

    def test_formatTime(self):
        timeObj = datetime.now().timetuple()
        timeFormat = "%H:%M:%S"
        expected = TimeUtil.format(timeObj, timeFormat)
        self.assertEqual(TimeUtil.formatTime(timeObj, timeFormat), expected)

    def test_formatDate(self):
        timeObj = datetime.now().timetuple()
        timeFormat = "%Y-%m-%d"
        expected = TimeUtil.format(timeObj, timeFormat)
        self.assertEqual(TimeUtil.formatDate(timeObj, timeFormat), expected)

    def test_formatDatetime(self):
        timeObj = datetime.now().timetuple()
        timeFormat = "%Y-%m-%d %H:%M:%S"
        expected = TimeUtil.format(timeObj, timeFormat)
        self.assertEqual(TimeUtil.formatDatetime(timeObj, timeFormat), expected)

    def test_getTimeObjByTimestamp(self):
        timestamp = int(round(time.time()))
        expected = time.localtime(timestamp)
        self.assertEqual(TimeUtil.getTimeObjByTimestamp(timestamp), expected)

    def test_getTimeObjNow(self):
        expected = time.localtime()
        self.assertEqual(TimeUtil.getTimeObjNow(), expected)

    def test_getNow(self):
        expected = TimeUtil.getTimeObjNow()
        self.assertEqual(TimeUtil.getNow(), expected)

    def test_getTimeObjByTimeStr(self):
        timeStr = "2023-11-22 12:34:56"
        timeFormat = "%Y-%m-%d %H:%M:%S"
        expected = time.strptime(timeStr, timeFormat)
        self.assertEqual(TimeUtil.getTimeObjByTimeStr(timeStr, timeFormat), expected)

    def test_getDateStrNow(self):
        timeFormat = "%Y-%m-%d"
        expected = TimeUtil.format(TimeUtil.getTimeObjNow(), timeFormat)
        self.assertEqual(TimeUtil.getDateStrNow(timeFormat), expected)

    def test_getDatetimeStrNow(self):
        timeFormat = "%Y-%m-%d %H:%M:%S"
        expected = TimeUtil.format(TimeUtil.getTimeObjNow(), timeFormat)
        self.assertEqual(TimeUtil.getDatetimeStrNow(timeFormat), expected)

    def test_getTimestamp(self):
        expected = int(round(time.time()))
        self.assertEqual(TimeUtil.getTimestamp(), expected)

    def test_getTimestampUseMillisecond(self):
        expected = int(round(time.time() * 1000))
        self.assertEqual(TimeUtil.getTimestampUseMillisecond(), expected)

    def test_formatTimestamp(self):
        timestamp = int(round(time.time()))
        timeFormat = "%Y-%m-%d %H:%M:%S"
        expected = TimeUtil.format(TimeUtil.getTimeObjByTimestamp(timestamp), timeFormat)
        self.assertEqual(TimeUtil.formatTimestamp(timestamp, timeFormat), expected)

    def test_getTimestampByTimeObj(self):
        timeObj = time.localtime()
        expected = time.mktime(timeObj)
        self.assertEqual(TimeUtil.getTimestampByTimeObj(timeObj), expected)

    def test_getTimestampByTimeStr(self):
        timeStr = "2023-11-22 12:34:56"
        timeFormat = "%Y-%m-%d %H:%M:%S"
        expected = TimeUtil.getTimestampByTimeObj(TimeUtil.getTimeObjByTimeStr(timeStr, timeFormat))
        self.assertEqual(TimeUtil.getTimestampByTimeStr(timeStr, timeFormat), expected)

    def test_calculateDaysBetween(self):
        startTimeStr = "2023-11-20"
        endTimeStr = "2023-11-25"
        expected = 5
        days = TimeUtil.calculateDaysBetween(startTimeStr, endTimeStr)
        self.assertEqual(days, expected)


if __name__ == '__main__':
    unittest.main()

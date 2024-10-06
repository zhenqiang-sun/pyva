import unittest

from pyva.client.feishu.FeishuRobotClient import FeishuRobotClient
from pyva.config.FeishuRobotConfig import FeishuRobotConfig


class FeishuRobotClientTest(unittest.TestCase):

    def test_sendText(self):
        FeishuRobotConfig.accessToken = "aaa"
        FeishuRobotConfig.secret = "bbb"

        client = FeishuRobotClient()
        content = "[飞书](https://www.feishu.cn)整合即时沟通、日历、音视频会议、云文档、云盘、工作台等功能于一体，成就组织和个人，更高效、更愉悦。"
        result = client.sendText(content)
        print(result)

    def test_sendMarkdown(self):
        FeishuRobotConfig.accessToken = "aaa"
        FeishuRobotConfig.secret = "bbb"

        client = FeishuRobotClient()
        title = "测试标题"
        text = "测试内容"

        title = "系统代码运行上报"
        text = '''[飞书](https://www.feishu.cn)整合即时沟通、日历、音视频会议、云文档、云盘、工作台等功能于一体，成就组织和个人，更高效、更愉悦。'''

        result = client.sendMarkdown(title, text)
        print(result)

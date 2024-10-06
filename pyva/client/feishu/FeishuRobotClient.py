import base64
import hashlib
import hmac
import time

import requests

from pyva.Global import G
from pyva.config.FeishuRobotConfig import FeishuRobotConfig


class FeishuRobotClient:
    """
    飞书消息机器人客户端
    官方文档：https://open.feishu.cn/document/client-docs/bot-v3/add-custom-bot
    """

    @staticmethod
    def verifyKeyword(content: str):
        """
        验证关键词
        :param content: 验证内容
        :return: True为通过 or False为未通过
        """

        if not FeishuRobotConfig.keywords:
            return True

        contains_keyword = any(keyword in content for keyword in FeishuRobotConfig.keywords)

        if not contains_keyword:
            G.logger.error("参数错误：关键词不匹配")
            return False

        return True

    @staticmethod
    def getSign():
        """
        获取签名
        :param timestamp: 时间戳
        :param secret: 密钥
        :return: 签名
        """
        timestamp = str(round(time.time()))
        secret = FeishuRobotConfig.secret

        # 拼接timestamp和secret
        string_to_sign = '{}\n{}'.format(timestamp, secret)
        hmac_code = hmac.new(string_to_sign.encode("utf-8"), digestmod=hashlib.sha256).digest()
        # 对结果进行base64处理
        sign = base64.b64encode(hmac_code).decode('utf-8')

        return timestamp, sign

    @staticmethod
    def sendMessage(data: dict):
        """
        基础方法-发送消息
        :param data:
        :return: 发送结果
        """

        webhookUrl = f"https://open.feishu.cn/open-apis/bot/v2/hook/{FeishuRobotConfig.accessToken}"

        if FeishuRobotConfig.secret:
            timestamp, sign = FeishuRobotClient.getSign()
            data["timestamp"] = timestamp
            data["sign"] = sign
        elif not FeishuRobotClient.verifyKeyword(str(data)):
            return None

        try:
            resp = requests.post(
                url=webhookUrl,
                json=data,
                timeout=1000
            )

            if resp.status_code == 200:
                return resp.json()
            else:
                return None
        except Exception as e:
            G.logger.error("调用错误：" + str(e))
            return None

    @staticmethod
    def sendText(content: str, atMobiles: list = [], atUserIds: list = [], isAtAll: bool = False):
        """
        发送文本消息

        :param content: 消息内容
        :param atMobiles:
        :param atUserIds:
        :param isAtAll:
        """

        data = {
            "msg_type": "text",
            "content": {
                "text": content
            },
        }

        return FeishuRobotClient.sendMessage(data)

    @staticmethod
    def sendMarkdown(title: str, text: str, atMobiles: list = [], atUserIds: list = [], isAtAll: bool = False):
        """
        发送Markdown消息

        :param title: 标题
        :param text: 内容
        :param atMobiles:
        :param atUserIds:
        :param isAtAll:
        """

        data = {
            "msg_type": "interactive",
            "card": {
                "config": {
                    "wide_screen_mode": True
                },
                "elements": [
                    {
                        "tag": "div",
                        "text": {
                            "tag": "lark_md",
                            "content": text
                        }
                    }
                ],
                "header": {
                    "title": {
                        "content": title,
                        "tag": "plain_text"
                    }
                }
            }
        }

        return FeishuRobotClient.sendMessage(data)

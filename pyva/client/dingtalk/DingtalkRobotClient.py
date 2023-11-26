import requests
from pyva.Global import G

from pyva.config.DingtalkRobotConfig import DingtalkRobotConfig


class DingtalkRobotClient:
    """
    钉钉消息推送机器人客户端
    官方文档：https://developers.dingtalk.com/document/app/custom-robot-access
    """

    @staticmethod
    def verify_keyword(content: str):
        """
        验证关键词
        :param content: 验证内容
        :return: True为通过 or False为未通过
        """

        contains_keyword = any(keyword in content for keyword in DingtalkRobotConfig.keywords)

        if not contains_keyword:
            G.logger.error("参数错误：关键词不匹配")
            return False

        return True

    @staticmethod
    def send_message(data: dict):
        """
        基础方法-发送消息
        :param data:
        :return: 发送结果
        """

        if not DingtalkRobotClient.verify_keyword(str(data)):
            return None

        webhook_url = "https://oapi.dingtalk.com/robot/send?access_token={accessToken}"
        url = webhook_url.format(accessToken=DingtalkRobotConfig.accessToken)

        try:
            resp = requests.post(
                url=url,
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
    def data_add_at(data, atMobiles: list = [], atUserIds: list = [], isAtAll: bool = False):
        """
        添加data的at信息
        :param data:
        :param atMobiles:
        :param atUserIds:
        :param isAtAll:
        :return:
        """

        if atMobiles or atUserIds or isAtAll:
            data["at"] = {
                "atMobiles": atMobiles,
                "atUserIds": atUserIds,
                "isAtAll": isAtAll
            }

        return data

    @staticmethod
    def send_text(content: str, atMobiles: list = [], atUserIds: list = [], isAtAll: bool = False):
        """
        发送文本消息

        :param content: 消息内容
        :param atMobiles:
        :param atUserIds:
        :param isAtAll:
        """

        data = {
            "msgtype": "text",
            "text": {
                "content": content
            },
        }

        DingtalkRobotClient.send_message(DingtalkRobotClient.data_add_at(data, atMobiles, atUserIds, isAtAll))

    @staticmethod
    def send_link(title: str, text: str, messageUrl: str, picUrl: str = None, atMobiles: list = [], atUserIds: list = [], isAtAll: bool = False):
        """
        发送链接消息

        :param title: 消息标题
        :param text: 消息内容。如果太长只会部分展示
        :param messageUrl: 点击消息跳转的URL
        :param picUrl: 图片URL
        :param atMobiles:
        :param atUserIds:
        :param isAtAll:
        """

        data = {
            "msgtype": "link",
            "link": {
                "title": title,
                "text": text,
                "messageUrl": messageUrl,
                "picUrl": picUrl,
            },
        }

        DingtalkRobotClient.send_message(DingtalkRobotClient.data_add_at(data, atMobiles, atUserIds, isAtAll))

    @staticmethod
    def send_markdown(title: str, text: str, atMobiles: list = [], atUserIds: list = [], isAtAll: bool = False):
        """
        发送Markdown消息

        :param title: 首屏会话透出的展示内容。
        :param text: markdown格式的消息。
        :param atMobiles:
        :param atUserIds:
        :param isAtAll:
        :return:
        """

        data = {
            "msgtype": "markdown",
            "markdown": {
                "title": title,
                "text": text
            },
        }

        DingtalkRobotClient.send_message(DingtalkRobotClient.data_add_at(data, atMobiles, atUserIds, isAtAll))

    @staticmethod
    def send_whole_action_card(title: str, text: str, singleTitle: str, singleURL: str, btnOrientation: str = None):
        """
        发送整体跳转ActionCard消息
        :param title: 首屏会话透出的展示内容。
        :param text: markdown格式的消息。
        :param singleTitle: 单个按钮的标题。
        :param singleURL: 点击消息跳转的URL，打开方式如下：
        :param btnOrientation: 0：按钮竖直排列、1：按钮横向排列
        :return:
        """

        data = {
            "msgtype": "actionCard",
            "actionCard": {
                "title": title,
                "text": text,
                "singleTitle": singleTitle,
                "singleURL": singleURL,
                "btnOrientation": btnOrientation,
            },
        }

        DingtalkRobotClient.send_message(data)

    @staticmethod
    def send_btns_action_card(title: str, text: str, btns: list, btnOrientation: str = None):
        """
        发送独立跳转ActionCard消息
        :param title: 首屏会话透出的展示内容。
        :param text: markdown格式的消息。
        :param btns: 按钮。
        :param btnOrientation: 0：按钮竖直排列、1：按钮横向排列
        :return:
        """

        data = {
            "msgtype": "actionCard",
            "actionCard": {
                "title": title,
                "text": text,
                "btns": btns,
                "btnOrientation": btnOrientation,
            },
        }

        DingtalkRobotClient.send_message(data)

    @staticmethod
    def send_feed_card(links: list):
        """
        发送FeedCard类型消息
        :param links:
        :return:
        """

        data = {
            "msgtype": "feedCard",
            "feedCard": {
                "links": links,
            },
        }

        DingtalkRobotClient.send_message(data)

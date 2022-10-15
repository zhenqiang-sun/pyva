import logging

from pyva.client.dingtalk.DingtalkOauth2Client import DingtalkOauth2Client
from pyva.config.DingtalkConfig import DingtalkConfig

logger = logging.getLogger('dingtalk')


class DingtalkContactClient:
    """
    钉钉通讯录Client
    """

    def __init__(self, dingtalkConfig: DingtalkConfig):
        self.dingtalkConfig = dingtalkConfig
        self.oauth = DingtalkOauth2Client(dingtalkConfig)

    def getDepartmentList(self, departmentId: int = None):
        """
        获取部门列表

        :doc https://open-dev.dingtalk.com/apiExplorer#/?devType=org&api=dingtalk.oapi.v2.department.listsub
        """

        url = "https://oapi.dingtalk.com/topapi/v2/department/listsub?access_token={token}"
        body = {
            "dept_id": departmentId
        }

        data = self.oauth.post(url=url, json=body)

        if data.get("errcode", -1) == 0:
            return data.get("result", [])
        else:
            logger.error(url)
            logger.error(body)
            logger.error(data)
            return None

    def getDepartmentUserList(self, departmentId: int = None, cursor: int = 0, size: int = 100):
        """
        获取部门用户基础信息

        :doc https://open-dev.dingtalk.com/apiExplorer#/?devType=org&api=dingtalk.oapi.user.listsimple
        :param departmentId 部门ID
        :param cursor 分页查询的游标
        :param size 分页长度
        """

        url = "https://oapi.dingtalk.com/topapi/user/listsimple?access_token={token}"

        body = {
            "dept_id": departmentId,
            "cursor": cursor,
            "size": size
        }

        data = self.oauth.post(url=url, json=body)

        if data.get("errcode", -1) == 0:
            return data.get("result", {}).get("list", [])
        else:
            logger.error(url)
            logger.error(body)
            logger.error(data)
            return None

    def getUser(self, userId: int) -> dict:
        """
        查询用户详情

        :doc https://open-dev.dingtalk.com/apiExplorer#/?devType=org&api=dingtalk.oapi.v2.user.get
        :param userId 用户ID
        """

        url = "https://oapi.dingtalk.com/topapi/v2/user/get?access_token={token}"

        body = {
            "userid": userId,
        }

        data = self.oauth.post(url=url, json=body)

        if data.get("errcode", -1) == 0:
            return data.get("result", {})
        else:
            logger.error(url)
            logger.error(body)
            logger.error(data)
            return None

import logging

from pyva.client.dingtalk.DingtalkOauth2Client import DingtalkOauth2Client
from pyva.config.DingtalkConfig import DingtalkConfig

logger = logging.getLogger('dingtalk')


class DingtalkYidaClient:
    """
    钉钉宜搭Client
    """

    apiUrlRoot = "https://api.dingtalk.com"
    appType = ""
    systemToken = ""
    userId = ""

    def __init__(self, appType: str, systemToken: str, userId: str, dingtalkConfig: DingtalkConfig):
        self.appType = appType
        self.systemToken = systemToken
        self.userId = userId

        self.dingtalkConfig = dingtalkConfig
        self.oauth = DingtalkOauth2Client(dingtalkConfig)

    def formFieldList(self, formUuid: str, version: str = None) -> list:
        """
        根据实例ID获取流程实例

        :doc https://open-dev.dingtalk.com/apiExplorer#/?devType=org&api=yida_1.0%23GetFormComponentDefinitionList
        :param formUuid 表单UUID
        :param version 表单版本
        """

        url = self.apiUrlRoot + "/v1.0/yida/forms/definitions/{appType}/{formUuid}?systemToken={systemToken}&userId={userId}&language=zh_CN".format(
            **{
                "appType": self.appType,
                "systemToken": self.systemToken,
                "userId": self.userId,
                "formUuid": formUuid,
            })
        if version:
            url += "&version={}".format(version)

        data = self.oauth.get(url=url)

        if data.get("result"):
            return data.get("result")
        else:
            logger.warning(data)
            return None

    def getInstance(self, instanceId: str) -> dict:
        """
        根据实例ID获取流程实例

        :doc https://open-dev.dingtalk.com/apiExplorer#/?devType=org&api=yida_1.0%23GetInstanceById
        :param instanceId 实例ID
        """

        url = self.apiUrlRoot + "/v1.0/yida/processes/instancesInfos/{}?appType={}&systemToken={}&userId={}".format(
            instanceId,
            self.appType,
            self.systemToken,
            self.userId)

        data = self.oauth.get(url=url)

        if data.get("data"):
            return data
        else:
            logger.warning(data)
            return None

    def createInstance(self, formUuid: str, processCode: str, formDataJson: str) -> str:
        """
        发起新的流程实例

        :doc https://open-dev.dingtalk.com/apiExplorer#/?devType=org&api=yida_1.0%23StartInstance
        :param formUuid 表单唯一编码
        :param processCode 表单唯一编码
        :param formDataJson 表单唯一编码
        """

        url = self.apiUrlRoot + "/v1.0/yida/processes/instances/start"

        body = {
            "appType": self.appType,
            "systemToken": self.systemToken,
            "userId": self.userId,
            "formUuid": formUuid,
            "processCode": processCode,
            "formDataJson": formDataJson,
        }

        data = self.oauth.post(url=url, json=body)

        if data and data.get("result"):
            return data.get("result")
        else:
            logger.warning(data)
            return None

    def updateInstance(self, instanceId: str, updateFormDataJson: str) -> bool:
        """
        更新流程实例

        :doc https://open-dev.dingtalk.com/apiExplorer#/?devType=org&api=yida_1.0%23UpdateInstance
        :param instanceId 实例ID
        :param updateFormDataJson 更新的表单数据
        """

        url = self.apiUrlRoot + "/v1.0/yida/processes/instances"

        body = {
            "appType": self.appType,
            "systemToken": self.systemToken,
            "userId": self.userId,
            "processInstanceId": instanceId,
            "updateFormDataJson": updateFormDataJson,
        }

        data = self.oauth.put(url=url, json=body)

        if not data:
            return True
        else:
            logger.warning(data)
            return False

    def terminateInstance(self, instanceId: str, ) -> bool:
        """
        更新流程实例

        :doc https://open-dev.dingtalk.com/apiExplorer#/?devType=org&api=yida_1.0%23TerminateInstance
        :param instanceId 实例ID
        """

        url = self.apiUrlRoot + "/v1.0/yida/processes/instances/terminate"

        body = {
            "appType": self.appType,
            "systemToken": self.systemToken,
            "userId": self.userId,
            "processInstanceId": instanceId,
        }

        data = self.oauth.put(url=url, json=body)

        if not data:
            return True
        else:
            logger.warning(data)
            return False

    def createComment(self, formInstanceId: str, userId: str, atUserId: str, content: str) -> str:
        """
        发起新的流程评论

        :doc https://open.dingtalk.com/document/orgapp-server/submit-comment
        :param formInstanceId 表单唯一编码
        :param userId 表单唯一编码
        :param atUserId 表单唯一编码
        :param content
        """

        url = self.apiUrlRoot + "/v1.0/yida/forms/remarks"

        body = {
            "appType": self.appType,
            "systemToken": self.systemToken,
            "replyId": '',
            "formInstanceId": formInstanceId,
            "userId": userId,
            "atUserId": atUserId,
            "content": content,
        }

        data = self.oauth.post(url=url, json=body)

        if not data:
            return True
        else:
            logger.warning(data)
            return False

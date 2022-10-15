import logging
import time

import requests

from pyva.config.DingtalkConfig import DingtalkConfig

logger = logging.getLogger('dingtalk')


class DingtalkOauth2Client:
    """
    钉钉授权Client
    """

    class Token:
        """
        Token对象
        """
        expireTime = 0.0
        accessToken = ""

    # token过期时间
    expireIn: int = 7200
    # token池
    tokenMap: dict = {}
    # 当前token
    token: Token = None

    def __init__(self, dingtalkConfig: DingtalkConfig):
        self.getAccessToken(dingtalkConfig)
        self.token = DingtalkOauth2Client.tokenMap.get(dingtalkConfig.appKey)

    @staticmethod
    def getAccessTokenByApi(dingtalkConfig: DingtalkConfig):
        """
        获取AccessToken通过Api

        :doc https://open-dev.dingtalk.com/apiExplorer#/?devType=org&api=oauth2_1.0%23GetAccessToken
        """

        url = "https://api.dingtalk.com/v1.0/oauth2/accessToken"
        body = {
            "appKey": dingtalkConfig.appKey,
            "appSecret": dingtalkConfig.appSecret
        }
        resp = requests.post(url=url, json=body)

        if resp.status_code == 200:
            return resp.json()
        else:
            logger.error(url)
            logger.error(body)
            logger.error(resp.text)
            return resp.json()

    @staticmethod
    def getAccessToken(dingtalkConfig: DingtalkConfig):
        """
        获取AccessToken优先缓存
        """

        token: DingtalkOauth2Client.Token = DingtalkOauth2Client.tokenMap.get(dingtalkConfig.appKey)

        if token and token.accessToken and token.expireTime > time.time():
            return token.accessToken

        resp = DingtalkOauth2Client.getAccessTokenByApi(dingtalkConfig)

        token = DingtalkOauth2Client.Token()
        token.accessToken = resp.get("accessToken", "")
        token.expireIn = resp.get("expireIn", 0)
        token.expireTime = time.time() + DingtalkOauth2Client.expireIn

        DingtalkOauth2Client.tokenMap[dingtalkConfig.appKey] = token

        return token.accessToken

    def request(self, method: str, url: str, headers: dict = None, **kwargs):
        if headers is None:
            headers = {}

        url = url.format(token=self.token.accessToken)
        headers["x-acs-dingtalk-access-token"] = self.token.accessToken

        resp = requests.request(method=method, url=url, headers=headers, **kwargs)

        if resp.status_code == 200:
            return resp.json()
        else:
            logger.error(resp.text)

            try:
                return resp.json()
            except:
                return None

    def get(self, url: str, header: dict = None, **kwargs):
        return self.request("get", url, header, **kwargs)

    def post(self, url: str, header: dict = None, **kwargs):
        return self.request("post", url, header, **kwargs)

    def put(self, url: str, header: dict = None, **kwargs):
        return self.request("put", url, header, **kwargs)

    def patch(self, url: str, header: dict = None, **kwargs):
        return self.request("patch", url, header, **kwargs)

    def delete(self, url: str, header: dict = None, **kwargs):
        return self.request("delete", url, header, **kwargs)

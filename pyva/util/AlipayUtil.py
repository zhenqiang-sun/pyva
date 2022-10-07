from alipay import BaseAliPay

from temp.AlipayConfig import AlipayConfig


class AlipayUtil:

    @staticmethod
    def getBaseAliPay(alipayConfig: AlipayConfig):
        """
        获取alipay基础操作对象
        :param alipayConfig:
        :return:
        """

        return BaseAliPay(
            appid=alipayConfig.appId,
            app_private_key_string="-----BEGIN RSA PRIVATE KEY-----\n{}\n-----END RSA PRIVATE KEY-----".format(
                alipayConfig.alipayPrivateKey),
            alipay_public_key_string="-----BEGIN PUBLIC KEY-----\n{}\n-----END PUBLIC KEY-----".format(
                alipayConfig.alipayPublicKey),
            sign_type="RSA2")

    @staticmethod
    def createQrcode(alipayConfig: AlipayConfig, deviceCode: str):
        """
        创建支付宝小程序码
        :param alipayConfig:
        :param deviceCode:
        :return:
        """

        alipay = AlipayUtil.getBaseAliPay(alipayConfig)

        resp = alipay.server_api(
            "alipay.open.app.qrcode.create",
            biz_content={
                "color": "0x000000",
                "describe": "A-{}".format(deviceCode),
                "query_param": "type=TcodeA",
                "size": "l",
                "url_param": "pages/t/b?d={}".format(deviceCode),
            }
        )

        if not resp.get("qr_code_url_circle_white"):
            print("Alipay createQrcode error.")
            print(resp)
            return None
        else:
            return resp["qr_code_url_circle_white"]

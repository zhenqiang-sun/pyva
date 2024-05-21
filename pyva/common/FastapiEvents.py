import os

from pyva.Global import G
from pyva.config.FastapiConfig import FastapiConfig
from pyva.util.TimeUtil import TimeUtil


class FastapiEvents:

    @staticmethod
    def startup():
        logoPath = G.staticPath + os.sep + 'logo.txt'
        with open(logoPath, "r", encoding="utf-8") as f:
            logoText = f.read()

        if FastapiConfig.https:
            protocol = "https"
        else:
            protocol = "http"

        info = f"""启动于：{TimeUtil.getDatetimeStrNow()}
{FastapiConfig.name} - {FastapiConfig.title}
{FastapiConfig.description}
{logoText}
Visit Root: {protocol}://localhost:{FastapiConfig.port}
"""
        if FastapiConfig.docs_url:
            info += f"Visit Docs: {protocol}://localhost:{FastapiConfig.port}{FastapiConfig.docs_url}"

        G.logger.warning(info)

    @staticmethod
    def shutdown():
        info = f"""停止于：{TimeUtil.getDatetimeStrNow()}
{FastapiConfig.name} - {FastapiConfig.title}
"""
        G.logger.warning(info)

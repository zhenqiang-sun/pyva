import datetime
import os

from pyva.Global import G
from pyva.config.FastapiConfig import FastapiConfig


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

        info = f"""{FastapiConfig.title} startup at {datetime.datetime.now()}
{FastapiConfig.title}, {FastapiConfig.description}
{logoText}
Visit Root: {protocol}://localhost:{FastapiConfig.port}
"""
        if FastapiConfig.docs_url:
            info += f"Visit Docs: {protocol}://localhost:{FastapiConfig.port}{FastapiConfig.docs_url}"

        G.logger.warning(info)

    @staticmethod
    def shutdown():
        G.logger.warning("{} shutdown at {}".format(
            FastapiConfig.title,
            datetime.datetime.now()
        ))

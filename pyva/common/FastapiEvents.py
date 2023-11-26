import datetime
import os

from src.Global import G
from src.config.AppConfig import AppConfig
from src.config.FastapiConfig import FastapiConfig


class FastapiEvents:

    @staticmethod
    def startup():
        logoPath = G.staticPath + os.sep + 'logo.txt'
        with open(logoPath, "r", encoding="utf-8") as f:
            logoText = f.read()

        if AppConfig.https:
            protocol = "https"
        else:
            protocol = "http"

        info = f"""{AppConfig.name} startup at {datetime.datetime.now()}
{FastapiConfig.title}, {FastapiConfig.description}
{logoText}
Visit Root: {protocol}://localhost:{AppConfig.port}
"""
        if FastapiConfig.docs_url:
            info += f"Visit Docs: {protocol}://localhost:{AppConfig.port}{FastapiConfig.docs_url}"

        G.logger.warning(info)

    @staticmethod
    def shutdown():
        G.logger.warning("{} shutdown at {}".format(
            AppConfig.name,
            datetime.datetime.now()
        ))

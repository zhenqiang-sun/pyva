import logging

from pyva.client.dingtalk.DingtalkRobotClient import DingtalkRobotClient
from pyva.client.feishu.FeishuRobotClient import FeishuRobotClient
from pyva.config.AppConfig import AppConfig
from pyva.util.IpUtil import IpUtil
from pyva.util.TimeUtil import TimeUtil


class LoggingHandler(logging.Handler):
    def __init__(self):
        logging.Handler.__init__(self)

    def emit(self, record):
        if AppConfig.env == "local":
            return

        if record.levelname not in ["ERROR", "WARNING"]:
            return

        self.log2dingtalk(record)
        self.log2feishu(record)

    def formatRecord(self, record):
        log_message = self.format(record)

        title = "系统代码运行上报"
        text = f'''{title}
- 级别：{record.levelname}
- 环境：{AppConfig.env}
- 服务：{AppConfig.name}
- 版本：{AppConfig.version}
- IP：{IpUtil.getHostIp()}
- 调试：{AppConfig.debug}
- 时间：{TimeUtil.formatTimestamp(record.created)}
- 线程：{record.thread}
- 文件：{record.filename}
- 行号：{record.lineno}
- 模块：{record.module}
- 函数：{record.funcName}
- 消息：
```
{log_message}
```
        '''

        return title, text

    def log2dingtalk(self, record):
        if not AppConfig.log2dingtalk:
            return

        if record.filename == "DingtalkRobotClient.py":
            return

        title, text = self.formatRecord(record)

        DingtalkRobotClient.sendMarkdown(
            title=title,
            text=text,
            # isAtAll=True
        )

    def log2feishu(self, record):
        if not AppConfig.log2feishu:
            return

        if record.filename == "FeishuRobotClient.py":
            return

        title, text = self.formatRecord(record)

        FeishuRobotClient.sendText(content=text)

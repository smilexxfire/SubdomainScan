import requests
import json
from abc import ABC, abstractmethod
from utils.tools import read_ini_config

class Notifier(ABC):
    @abstractmethod
    def send_message(self, message):
        pass




class DingTalkNotifier(Notifier):
    __instance = None

    @staticmethod
    def get_instance(access_token):
        if DingTalkNotifier.__instance is None:
            DingTalkNotifier(access_token)
        return DingTalkNotifier.__instance

    def __init__(self, access_token):
        if DingTalkNotifier.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self.url = 'https://oapi.dingtalk.com/robot/send?access_token=' + access_token
            self.headers = {'Content-Type': 'application/json;charset=utf-8'}
            DingTalkNotifier.__instance = self

    def send_message(self, message):
        data = {
            "msgtype": "text",
            "text": {
                "content": message
            }
        }
        response = requests.post(self.url, headers=self.headers, data=json.dumps(data))
        return response.status_code


class NotifierFactory:
    @staticmethod
    def get_notifier():
        notifier_name = read_ini_config("notifier", "origin")
        if notifier_name == 'dingding':
            access_token = read_ini_config("notifier", "dingding_token")
            return DingTalkNotifier.get_instance(access_token)
        else:
            raise ValueError("Invalid notifier name.")


# 示例用法
# notifier = NotifierFactory.get_notifier()
# response = notifier.send_message("[小小火牛逼]\n测试消息")
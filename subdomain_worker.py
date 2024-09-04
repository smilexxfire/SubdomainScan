# -*- coding: UTF-8 -*-
'''
@Project ：subdomainMonitor 
@File    ：subdomain_worker.py
@IDE     ：PyCharm 
@Author  ：smilexxfire
@Date    ：2024/7/29 11:36 
'''

import json
from common.database.consumer import RabbitMQConsumer
from modules.subdomain import Subdomain
from modules.heartbeat import Heartbeat
from config.settings import HEARTBEAT_OPEN
class SubdomainWorker(RabbitMQConsumer):
    def __init__(self, queue_name):
        super().__init__(queue_name)

    def task_handle(self):
        task = json.loads(self.message)
        subdomain = Subdomain(task)
        subdomain.run()


if __name__ == '__main__':
    # 启动心跳程序
    if HEARTBEAT_OPEN == "true":
        hb = Heartbeat("心跳线程")
        hb.start()
    # 启动子域名扫描服务
    worker = SubdomainWorker("subdomain_custom_task")
    worker.start_consuming()
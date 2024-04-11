import json

import pika

from config.config import SUBDOMAIN_MODULE, SUBDOMAIN_ASSERT_NAME
from modules.database import RabbitMQConnection
from utils.tools import read_ini_config

from modules.database import conn_db

class RabbitMQProducer:
    def __init__(self):
        self.connection = RabbitMQConnection.get_connection()
        self.channel = self.connection.channel()
        self.queue_name = read_ini_config("rabbitmq", "queue_name")

        # 声明队列
        self.channel.queue_declare(queue=self.queue_name)

    def publish_message(self, message):
        # 发布消息
        self.channel.basic_publish(exchange='', routing_key=self.queue_name, body=message)
        print(f" [x] Sent '{message}'")

    def purge_queue(self):
        # 清空队列
        self.channel.queue_purge(queue=self.queue_name)
        print(f"Queue '{self.queue_name}' purged")

    def publish_subdomain_task(self):
        # 获取启用的扫描模块
        scan_modules = SUBDOMAIN_MODULE.split(",")
        scan_modules = list(map(str.strip, scan_modules))  # 消除无效字符

        # 获取需要扫描的资产名称
        query = {}
        if SUBDOMAIN_ASSERT_NAME != "all":
            assert_names = SUBDOMAIN_ASSERT_NAME.split(",")
            query = {"assert_name": {"$in": assert_names}}
        collection = conn_db("asserts")
        records = collection.find(query)
        datas = list()
        for record in records:
            datas.append(record)

        # 发布扫描任务
        for data in datas:
            for module_name in scan_modules:
                task = {
                    "assert_name": data["assert_name"],
                    "domain": data["domain"],
                    "module_name": module_name
                }
                self.publish_message(json.dumps(task))



# 使用示例
# producer = RabbitMQProducer()
# producer.publish_message('Your message to be sent')

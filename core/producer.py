import json

import pika
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
        db = conn_db("asserts")
        # 查询所有资产的情况
        if read_ini_config("subdomain", "assert_name") == "all":
            results = db.find()
            for result in results:
                data = {
                    "assert_name": result["assert_name"],
                    "domain": result["domain"]
                }
                self.publish_message(json.dumps(data))
            return
        # 查询部分资产的情况
        assert_name_list = read_ini_config("subdomain", "assert_name").split(",")
        for assert_name in assert_name_list:
            assert_name = assert_name.strip()
            results = db.find({"assert_name": assert_name})
            for result in results:
                data = {
                    "assert_name": assert_name,
                    "domain": result["domain"]
                }
                print(data)
                self.publish_message(json.dumps(data))



# 使用示例
# producer = RabbitMQProducer()
# producer.publish_message('Your message to be sent')

import json

from config import settings
from modules.database.db import RabbitMQConnection

from modules.database.db import conn_db

class RabbitMQProducer:
    def __init__(self, queue_name):
        self.connection = RabbitMQConnection.get_connection()
        self.channel = self.connection.channel()
        self.queue_name = queue_name

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




if __name__ == '__main__':
    # 使用示例
    producer = RabbitMQProducer("subdomain")
    producer.publish_message('Your message to be sent')

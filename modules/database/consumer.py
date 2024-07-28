import abc
import json
import time
from abc import ABC

import pika

from config.log import logger
from config import settings
from modules.database.db import RabbitMQConnection

class RabbitMQConsumer(ABC):
    def __init__(self, queue_name):
        self.queue_name = queue_name
        self.message = str()

    @abc.abstractmethod
    def task_handle(self):
        pass


    def callback(self, ch, method, properties, body):
        print(f" [x] Received {body}")
        # 手动确认消息
        ch.basic_ack(delivery_tag=method.delivery_tag)
        print("Message acknowledged")
        self.message = body
        # 处理接收到的消息
        self.task_handle()

    def start_consuming(self):
        try:
            connection = RabbitMQConnection.get_connection()
            channel = connection.channel()

            # 声明队列
            channel.queue_declare(queue=self.queue_name)

            # 设置消费者的手动确认和消息预取
            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(queue=self.queue_name, on_message_callback=self.callback)

            print(' [*] Waiting for messages. To exit, press CTRL+C')
            channel.start_consuming()
        except pika.exceptions.StreamLostError as e:
            logger.error(f"Stream connection lost: {e}")
            # 进行重试逻辑
            print("Reconnecting...")
            time.sleep(5)  # 重试等待时间
            self.start_consuming()

if __name__ == '__main__':
    # 使用示例
    consumer = RabbitMQConsumer()
    consumer.start_consuming()
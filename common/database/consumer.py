import abc
import time
from abc import ABC

import pika
from common.database.db import RabbitMQConnection
from config.log import logger

class RabbitMQConsumer(ABC):
    def __init__(self, queue_name):
        self.queue_name = queue_name

    @abc.abstractmethod
    def task_handle(self):
        pass

    def callback(self, ch, method, properties, body):
        logger.log("INFOR",f" [x] Received {body}")
        # 手动确认消息
        ch.basic_ack(delivery_tag=method.delivery_tag)
        logger.log("INFOR", "Message acknowledged")
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

            logger.log("INFOR", ' [*] Waiting for messages. To exit, press CTRL+C')
            channel.start_consuming()
        except pika.exceptions.StreamLostError as e:
            logger.log("ERROR",f"Stream connection lost: {e}")
            # 进行重试逻辑
            logger.log("ERROR","Reconnecting...")
            time.sleep(5)  # 重试等待时间
            self.start_consuming()
        except pika.exceptions.AMQPHeartbeatTimeout as e:
            logger.log("ERROR",f"Stream connection lost: {e}")
            # 进行重试逻辑
            logger.log("ERROR","Reconnecting...")
            time.sleep(5)  # 重试等待时间
            self.start_consuming()

if __name__ == '__main__':
    # 使用示例
    consumer = RabbitMQConsumer()
    consumer.start_consuming()
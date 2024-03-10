import json
import time

import pika

from config.config import logger
from modules.database import RabbitMQConnection
from modules.subdomain import Subdomain
from utils.tools import read_ini_config

class RabbitMQConsumer:
    def __init__(self):
        pass

    def callback(self, ch, method, properties, body):
        print(f" [x] Received {body}")
        # 处理接收到的消息，开始子域名扫描任务
        data = json.loads(body)
        print(data)
        # 手动确认消息™
        ch.basic_ack(delivery_tag=method.delivery_tag)
        print("Message acknowledged")
        # 任务处理
        Subdomain.start(data)


    def start_consuming(self):
        try:
            connection = RabbitMQConnection.get_connection()
            channel = connection.channel()
            queue_name = read_ini_config("rabbitmq", "queue_name")

            # 声明队列
            channel.queue_declare(queue=queue_name)

            # 设置消费者的手动确认和消息预取
            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(queue=queue_name, on_message_callback=self.callback)

            print(' [*] Waiting for messages. To exit, press CTRL+C')
            channel.start_consuming()
        except pika.exceptions.StreamLostError as e:
            logger.error(f"Stream connection lost: {e}")
            # 进行重试逻辑
            print("Reconnecting...")
            time.sleep(5)  # 重试等待时间
            self.start_consuming()

# # 使用示例
# consumer = RabbitMQConsumer()
# consumer.start_consuming()
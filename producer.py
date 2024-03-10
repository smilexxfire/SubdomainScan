import json

from core.producer import RabbitMQProducer

producer = RabbitMQProducer()
producer.purge_queue()
producer.publish_subdomain_task()
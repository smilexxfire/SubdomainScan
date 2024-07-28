from modules.database.producer import RabbitMQProducer

producer = RabbitMQProducer()
producer.purge_queue()
producer.publish_subdomain_task()
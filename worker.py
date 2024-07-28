from modules.database.consumer import RabbitMQConsumer

consumer = RabbitMQConsumer()
consumer.start_consuming()

from modules.database import RabbitMQConnection

connection = RabbitMQConnection.get_connection()
channel = connection.channel()

# 声明队列
queue_name = 'my_queue'
channel.queue_declare(queue=queue_name)

def callback(ch, method, properties, body):
    print(f"Received message: {body}")

    # 手动确认消息
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print("Message acknowledged")

# 设置消费者的手动确认和消息预取
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=queue_name, on_message_callback=callback)

print('Waiting for messages. To exit, press CTRL+C')
channel.start_consuming()

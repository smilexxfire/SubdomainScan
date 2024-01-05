import json

from modules.database import RabbitMQConnection
# 使用单例模式获取连接
connection = RabbitMQConnection.get_connection()

# 创建一个通道
channel = connection.channel()

# 声明队列
queue_name = 'my_queue'
channel.queue_declare(queue=queue_name)

message = {
    "name": "dsadsa",
    "age": "asd"
}
message = json.dumps(message)
channel.basic_publish(exchange='', routing_key=queue_name, body=message)
print(f" [x] Sent '{message}'")

channel.basic_publish(exchange='', routing_key=queue_name, body=message)
print(f" [x] Sent '{message}'")

channel.basic_publish(exchange='', routing_key=queue_name, body=message)
print(f" [x] Sent '{message}'")

connection.close()
import pika
from pymongo import MongoClient
from config import settings
from config.log import logger
class RabbitMQConnection:
    _instance = None
    _connection = None

    username = settings.RABBITMQ_USER
    password = settings.RABBITMQ_PASSWORD
    host = settings.RABBITMQ_HOST
    port = settings.RABBITMQ_PORT

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def get_connection(cls):
        if cls._instance is None:
            cls._instance = RabbitMQConnection()
        if cls._connection is None or cls._connection.is_closed:
            cls._connection = cls._instance.create_connection()
        return cls._connection

    @classmethod
    def create_connection(cls):
        while True:
            try:
                credentials = pika.PlainCredentials(cls.username, cls.password)
                parameters = pika.ConnectionParameters(cls.host, cls.port, '/', credentials,
                                                       connection_attempts=3,  # 最大连接尝试次数
                                                       retry_delay=5) # 重试间隔时间，单位为秒
                return pika.BlockingConnection(parameters)
            except pika.exceptions.AMQPConnectionError as e:
                logger.log("ERROR", f"AMQPConnectionError: {e}")
                logger.log("INFOR", "尝试重连....")


class ConnMongo(object):
    username = settings.MONGO_USER
    password = settings.MONGO_PASSWORD
    host = settings.MONGO_HOST
    port = settings.MONGO_PORT

    def __new__(self):
        if not hasattr(self, 'instance'):
            uri = f'mongodb://{self.username}:{self.password}@{self.host}:{self.port}' \
                if self.username and self.password else f'mongodb://{self.host}:{self.port}'
            self.instance = super(ConnMongo, self).__new__(self)
            self.instance.conn = MongoClient(uri)
        return self.instance


def conn_db(collection):
    db_name = settings.MONGO_DATABASE
    conn = ConnMongo().conn
    if db_name:
        return conn[db_name][collection]

if __name__ == '__main__':
    # 测试代码
    conn_db("subdomain")
    RabbitMQConnection.get_connection()
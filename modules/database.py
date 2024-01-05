import time

import pika
from utils.tools import *

class RabbitMQConnection:
    _instance = None
    _connection = None

    username = read_ini_config("rabbitmq", "username")
    password = read_ini_config("rabbitmq", "password")
    host = read_ini_config("rabbitmq", "host")
    port = read_ini_config("rabbitmq", "port")

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
        credentials = pika.PlainCredentials(cls.username, cls.password)
        parameters = pika.ConnectionParameters(cls.host, cls.port, '/', credentials)
        return pika.BlockingConnection(parameters)


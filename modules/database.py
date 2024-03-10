import time

import pika
from utils.tools import *
from pymongo import MongoClient

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

class ConnMongo(object):
    username = read_ini_config("mongodb", "username")
    password = read_ini_config("mongodb", "password")
    host = read_ini_config("mongodb", "host")
    port = read_ini_config("mongodb", "port")
    def __new__(self):
        if not hasattr(self, 'instance'):
            uri = f'mongodb://{self.username}:{self.password}@{self.host}:{self.port}' \
                if self.username and self.password else f'mongodb://{self.host}:{self.port}'
            self.instance = super(ConnMongo, self).__new__(self)
            self.instance.conn = MongoClient(uri)
        return self.instance


def conn_db(collection):
    db_name = read_ini_config("mongodb", "db")
    conn = ConnMongo().conn
    if db_name:
        return conn[db_name][collection]

# db = conn_db("asserts")
# results = db.find()
# rs = list(results)
# for _ in rs:
#     print(_)
# print(len(rs))
# print(type(rs[0]))
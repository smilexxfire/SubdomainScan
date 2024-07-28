from modules.database.consumer import RabbitMQConsumer

class SubdomainWorker(RabbitMQConsumer):
    def __init__(self, queue_name):
        super().__init__(queue_name)

    def task_handle(self):
        print("开始子域名扫描任务")


if __name__ == '__main__':
    worker = SubdomainWorker("subdomain")
    worker.start_consuming()
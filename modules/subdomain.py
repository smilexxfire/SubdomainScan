from config.log import logger
from modules.scan import subfinder, xray


class Subdomain(object):
    DB_COLLECTION = "subdomain"

    def __init__(self, task: dict):
        self.task = task
        self.modules = list()
        self.collect_funcs = list()
        pass

    def run(self):
        """子域名扫描入口函数

        :param task: 待扫描任务字典，assert_name、domain、module_name
        :return:
        """
        logger.log('INFOR', f'Start collecting subdomains of {self.task["domain"]}')
        if self.task["module_name"] == "subfinder":
            subfinder.run(self.task)
        elif self.task["module_name"] == "xray":
            xray.run(self.task)


if __name__ == '__main__':
    subdomain = Subdomain({"domain": "xxf.world", "assert_name": "测试", "module_name": "subfinder"})
    subdomain.run()
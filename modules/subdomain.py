from config.log import logger
from modules.subdomainscan import subfinder, amass


class Subdomain(object):
    DB_COLLECTION = "subdomain"

    def __init__(self, task: dict):
        self.task = task

    def run(self):
        """子域名扫描模块入口函数

        :param task: 待扫描任务字典，assert_name、domain、module_name
        :return:
        """
        logger.log('INFOR', f'Start collecting subdomains of {self.task["domain"]}')
        if self.task["module_name"] == "subfinder":
            subfinder.run(self.task["domain"], self.task["task_id"])
        elif self.task["module_name"] == "amass":
            amass.run(self.task["domain"], self.task["task_id"])
        logger.log('INFOR', f'Finished collecting subdomains of {self.task["domain"]}')


if __name__ == '__main__':
    subdomain = Subdomain({"domain": "xxf.world", "module_name": "subfinder", "task_id": "123123"})
    subdomain.run()
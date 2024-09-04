import json
import subprocess
from common.module import Module
from common.utils import rename_dict_key
from config.log import logger
class Subfinder(Module):
    def __init__(self, domain:str):
        """

        :param domain: 需要扫描的域名
        """
        self.module = "subdomainscan"
        self.source = "subfinder"
        self.collection = "subdomain"
        self.domain = domain
        Module.__init__(self, domain)

    def do_scan(self):
        """
        执行扫描任务

        @return:
        """
        cmd = [self.execute_path, "-d", self.domain, "-oJ", "-o", self.result_file]
        subprocess.run(cmd)

    def deal_data(self):
        """
        处理扫描结果, 提取出所有子域

        @return:
        """
        # 从文件中读取数据
        logger.log("INFOR", "Start deal data process")
        with open(self.result_file, "r") as f:
            datas = f.readlines()
            json_list = [json.loads(data) for data in datas]
            for data in json_list:
                rename_dict_key(data, "input", "domain")
                rename_dict_key(data, "host", "subdomain")
                del data["source"]
                data["source"] = self.source

        self.results = json_list

    def save_db(self):
        super().save_db("subdomain")


    def run(self):
        """
        入口执行函数

        @return:
        """
        self.begin()
        self.do_scan()
        self.deal_data()
        self.save_db()
        self.finish()
        self.delete_temp()

def run(target:str):
    """
    类调用统一入口
    
    @return: 
    """
    subfinder = Subfinder(target)
    subfinder.run()

if __name__ == '__main__':
    run(target="xxf.world")

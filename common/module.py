"""
Module base class
"""

import json
import threading
import time

import requests
from config.log import logger
from config import settings
from common import utils

lock = threading.Lock()


class Module(object):
    def __init__(self):
        self.module = 'Module'
        self.source = 'BaseModule'
        # self.cookie = None
        # self.header = dict()
        # self.proxy = None
        # self.delay = 1  # 请求睡眠时延
        # self.timeout = settings.request_timeout_second  # 请求超时时间
        # self.verify = settings.request_ssl_verify  # 请求SSL验证
        self.domain = str()  # 当前进行子域名收集的主域
        self.subdomains = set()  # 存放发现的子域
        self.results = list()  # 存放模块结果
        self.start = time.time()  # 模块开始执行时间
        self.end = None  # 模块结束执行时间
        self.elapse = None  # 模块执行耗时

    def begin(self):
        """
        begin log
        """
        logger.log('DEBUG', f'Start {self.source} module to '
                            f'collect subdomains of {self.domain}')

    def finish(self):
        """
        finish log
        """
        self.end = time.time()
        self.elapse = round(self.end - self.start, 1)
        logger.log('DEBUG', f'Finished {self.source} module to '
                            f'collect {self.domain}\'s subdomains')
        logger.log('INFOR', f'{self.source} module took {self.elapse} seconds '
                            f'found {len(self.subdomains)} subdomains')
        logger.log('DEBUG', f'{self.source} module found subdomains of {self.domain}\n'
                            f'{self.subdomains}')

    def save_json(self):
        """
        Save the results of each module as a json file

        :return bool: whether saved successfully
        """
        if not settings.save_module_result:
            return False
        logger.log('TRACE', f'Save the subdomain results found by '
                            f'{self.source} module as a json file')
        path = settings.result_save_dir.joinpath(self.domain, self.module)
        path.mkdir(parents=True, exist_ok=True)
        name = self.source + '.json'
        path = path.joinpath(name)
        with open(path, mode='w', errors='ignore') as file:
            result = {'domain': self.domain,
                      'name': self.module,
                      'source': self.source,
                      'elapse': self.elapse,
                      'find': len(self.subdomains),
                      'subdomains': list(self.subdomains),
                      'infos': self.infos}
            json.dump(result, file, ensure_ascii=False, indent=4)
        return True


    def save_db(self):
        """
        Save module results into the database
        """
        logger.log('DEBUG', f'Saving results to database')
        lock.acquire()
        db = Database()
        db.create_table(self.domain)
        db.save_db(self.domain, self.results, self.source)
        db.close()
        lock.release()

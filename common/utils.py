
import configparser
import os
import requests
import socket

def get_hostname():
    try:
        hostname = socket.gethostname()
        return hostname
    except socket.error as err:
        print(f"Unable to get hostname: {err}")
        return None

def read_ini_config(section_name, key_name, file_name=os.path.dirname(os.path.abspath(__file__)) + "/../config/default.ini"):
    # 先从环境变量获取
    value = os.getenv(f"{section_name}_{key_name}")
    if value is not None:
        return value
    # 再从配置文件获取
    try:
        config = configparser.ConfigParser()
        config.read(file_name, encoding='utf-8')
        value = config.get(section_name, key_name)
        return value
    except:
        return None
def get_external_ip():
    try:
        response = requests.get('https://httpbin.org/ip')
        response.raise_for_status()  # 检查请求是否成功
        ip = response.json()['origin']
        return ip
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None


def rename_dict_key(dict_obj, old_key, new_key):
    """
    将字典中的指定键名 old_key 修改为 new_key，但对应的值不变。

    Args:
        dict_obj (dict): 需要修改键名的字典对象。
        old_key (str): 需要修改的键名。
        new_key (str): 修改后的键名。

    Returns:
        dict: 修改键名后的字典对象。

    """
    if old_key in dict_obj:
        dict_obj[new_key] = dict_obj.pop(old_key)
    return dict_obj

def delete_file_if_exists(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)


def is_chinese(string):
    """
    检查整个字符串是否包含中文
    :param string: 需要检查的字符串
    :return: bool
    """
    for ch in string:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True

    return False

if __name__ == '__main__':
    print(is_chinese("测试"))
    print(is_chinese("sdwdas"))
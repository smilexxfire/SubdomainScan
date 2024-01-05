
import configparser
import os

def read_ini_config(section_name, key_name, file_name=os.path.dirname(os.path.abspath(__file__)) + "/../config/default.ini"):
    config = configparser.ConfigParser()
    config.read(file_name)
    value = config.get(section_name, key_name)
    return value

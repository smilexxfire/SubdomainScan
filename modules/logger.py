import logging
from pathlib import Path
from utils.tools import read_ini_config


current_script_path = Path(__file__).resolve()
log_file = str(current_script_path.parent.parent) + "/" + read_ini_config("basic", "log_file")
class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Logger(metaclass=Singleton):
    def __init__(self, log_file=log_file):
        self.log_file = log_file
        self._configure_logger()

    def _configure_logger(self):
        log_format = '%(asctime)s - %(levelname)s - %(message)s'
        logging.basicConfig(filename=self.log_file, level=logging.INFO, format=log_format, datefmt='%Y-%m-%d %H:%M:%S')
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        console.setFormatter(logging.Formatter(log_format))
        logging.getLogger('').addHandler(console)

    def info(self, message):
        logging.info(message)

    def error(self, message):
        logging.error(message)

    def warning(self, message):
        logging.warning(message)

    def debug(self, message):
        logging.debug(message)

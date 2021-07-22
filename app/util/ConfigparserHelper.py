import configparser
from app import config_location
import os

CONFIG_FILE_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), config_location)
class ConfigparserHelper:
    def __init__(self):
        self.config = configparser.ConfigParser(interpolation=None)
        self.config.read(CONFIG_FILE_PATH)

    def getValue(self, section, key):
        return self.config.get(section, key)


if __name__ == '__main__':
    ch = ConfigparserHelper()
    ans = ch.getValue('regx', 'delimiter')
    print(ans)
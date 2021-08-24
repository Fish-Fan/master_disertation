import configparser
from app import config_location
import os
import re

CONFIG_FILE_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), config_location)
class ConfigparserHelper:
    def __init__(self):
        self.config = configparser.ConfigParser(interpolation=None)
        self.config.read(CONFIG_FILE_PATH)

    def getValue(self, section, key):
        return self.config.get(section, key)

    def getTransformationTypesAndSemanticRole(self):
        ans = {}
        ans['int'] = self.getValue('transformation_type', 'int')
        ans['float'] = self.getValue('transformation_type', 'float')
        ans['email'] = self.getValue('semantic_role', 'email')
        ans['postal'] = self.getValue('semantic_role', 'postal')
        return ans


if __name__ == '__main__':
    ch = ConfigparserHelper()
    ans = ch.getTransformationTypesAndSemanticRole()
    print(ans)
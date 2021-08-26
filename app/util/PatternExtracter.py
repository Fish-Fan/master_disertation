import re
from collections import defaultdict
from app.util.ConfigparserHelper import ConfigparserHelper

class PatternExtracter:
    def __init__(self, strList):
        self.strList = strList

    def str_to_regex(self, id):
        x = re.escape(id)
        ch = ConfigparserHelper()
        delimiter = ch.getValue('regx', 'delimiter')
        # replace delimiter with (delimiter)
        x = re.sub(r'([^a-zA-Z0-9]+['+ delimiter +']*[\s]*)', r'(\1)', x)
        # replace words with [a-zA-Z]+
        x = re.sub(r'[a-zA-Z]+', r'([A-Z]+)', x)
        # replace digits with [0-9]+
        x = re.sub(r'[0-9]+', r'([0-9]+)', x)
        return '^' + x + '$'

    def determineRegex(self):
        patterns = defaultdict(list)
        for id in self.strList:
            pattern = self.str_to_regex(id)
            patterns[pattern].append(id)

        return patterns
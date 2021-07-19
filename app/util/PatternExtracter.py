import re
from collections import defaultdict

class PatternExtracter:
    def __init__(self, strList):
        self.strList = strList

    def str_to_regex(self, id):
        x = re.escape(id)
        x = re.sub(r'([^a-zA-Z0-9]+[_~+!@#$%^&*./-]*[\s]*)', r'(\1)', x)
        x = re.sub(r'[a-zA-Z]+', r'([A-Z)]+)', x)
        x = re.sub(r'[0-9]+', r'([0-9]+)', x)
        return '^' + x + '$'

    def determineRegex(self):
        patterns = defaultdict(list)
        for id in self.strList:
            pattern = self.str_to_regex(id)
            patterns[pattern].append(id)

        return patterns
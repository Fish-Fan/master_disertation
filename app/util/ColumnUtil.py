import re
from collections import defaultdict, OrderedDict

class ColumnUtil:
    def __init__(self, column_df):
        self.column_df = column_df.dropna()

    def getMostFrequency(self):
        return self.column_df.mode()[0]

    def guessColumnType(self):
        types = {
            'int': r'^-?\d+$',
            'float': r'^\d+.{1}\d+$',
            'email': r'^([a-zA-Z0-9._-]+)@([a-zA-Z0-9]+).([a-zA-Z0-9]+)$',
            'postal': r'^[A-Z]{1,2}[0-9]{1,2}[A-Z]?\s?[0-9][A-Z]{2}$'
        }

        d = defaultdict(list)
        for value in list(self.column_df):
            count = 0
            for name, reg in types.items():
                if re.match(reg, str(value)):
                    d[name].append(value)
                    count += 1
            if count == 0:
                d['string'].append(value)
        d = OrderedDict(sorted(d.items(), key=lambda t: t[1], reverse=True))
        for key, matched_arr in d.items():
            if len(matched_arr) > len(self.column_df) // 2:
                return {'type': key, 'matchValues': matched_arr}
            else:
                return {'type': 'string', 'matchValues': matched_arr}


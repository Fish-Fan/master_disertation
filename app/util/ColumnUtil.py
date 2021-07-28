import re
from collections import defaultdict, OrderedDict

class ColumnUtil:
    def __init__(self, column_df):
        self.column_df = column_df.dropna()

    def getMostFrequency(self):
        if len(self.column_df) > 0:
            return self.column_df.mode()[0]
        else:
            return ""

    def guessColumnType(self):
        column_type = {}
        h = self.getColumnTypeHistogram()
        for type, matched_obj in h.items():
            if matched_obj['count'] > len(self.column_df) // 2:
                column_type['type'] = type
                column_type['matchValues'] = matched_obj['raw_data']
            else:
                column_type['type'] = 'string'
                column_type['matchValues'] = h.get('string')['raw_data']
            break
        return column_type

    def getColumnTypeHistogram(self, type=None):
        regex_list = {'int': r'^-?\d+$', 'float': r'^[0-9]+[.]{1}[0-9]+$',
                      'email': r'^([a-zA-Z0-9._-]+)@([a-zA-Z0-9]+).([a-zA-Z0-9]+)([.uk]*)$',
                      'postal': r'^[A-Z]{1,2}[0-9]{1,2}[A-Z]?\s?[0-9][A-Z]{2}$'}
        d = defaultdict(list)
        # in case of NoneType occurrence
        d['string'] = []
        for value in list(self.column_df):
            if type:
                name, reg = type, regex_list.get(type)
                if re.match(reg, str(value)):
                    d[name].append(value)
                else:
                    d['string'].append(value)
            else:
                count = 0
                for name, reg in regex_list.items():
                    if re.match(reg, str(value)):
                        d[name].append(value)
                        count += 1
                if count == 0:
                    d['string'].append(value)
        self._check_is_category_type_(d)
        d = self._construct_return_value_(d)
        return d

    def _check_is_category_type_(self, d):
        if len(self.column_df) > 0:
            category_count = len(self.column_df.value_counts().keys())
            value_count = len(self.column_df)
            if 1 - category_count / value_count >= 0.9:
                # empty string ans
                d['category'] = d['string']
                d['string'] = []

    def _construct_return_value_(self, d):
        ans = {}
        for dataType, matchedArr in d.items():
            ans[dataType] = {'raw_data': matchedArr,'count': len(matchedArr)}
        return OrderedDict(sorted(ans.items(), key=lambda t: t[1]['count'], reverse=True))



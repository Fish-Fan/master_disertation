import re
from collections import defaultdict, OrderedDict
from app.util.ConfigparserHelper import ConfigparserHelper

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
        # get column histogram
        h = self.getColumnTypeHistogram()
        for type, matched_obj in h.items():
            # check is over half of non-missing values
            if matched_obj['count'] > len(self.column_df) // 2:
                column_type['type'] = type
                column_type['matchValues'] = matched_obj['raw_data']
            else:
                column_type['type'] = 'string'
                column_type['matchValues'] = h.get('string')['raw_data']
            break
        return column_type

    def getColumnTypeHistogram(self, type=None):
        # read regx from configuration
        ch = ConfigparserHelper()
        regex_list = ch.getTransformationTypesAndSemanticRole()
        d = defaultdict(list)
        # initialise
        d['string'] = []
        if type:
            d[type] = []
        # iterate value in this column
        for value in list(self.column_df):
            # try to match value with designated type
            if type:
                name, reg = type, regex_list.get(type)
                if re.match(reg, str(value)):
                    d[name].append(value)
                else:
                    d['string'].append(value) # degenerate to string
            else:
                count = 0
                # try to match each type or semantic role
                for name, reg in regex_list.items():
                    if re.match(reg, str(value)):
                        d[name].append(value)
                        count += 1
                # degenerate to string
                if count == 0:
                    d['string'].append(value)
        # check whether can upgrade to categorical column
        self._check_is_category_type_(d)
        # construct return value
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



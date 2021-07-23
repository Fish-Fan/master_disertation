import numpy as np
import pandas as pd
from pandas_profiling import ProfileReport
import os
import math
from .. import report_html_location
from datetime import datetime
from collections import OrderedDict
from app.util.PatternExtracter import PatternExtracter
from app.util.ColumnUtil import ColumnUtil

REPORT_HTML_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), report_html_location)

class Profiling_util:
    def __init__(self, source, data_frame=None):
        self.source = source
        if source:
            self.df = pd.read_csv(self.source)
        else:
            self.df = data_frame

    def getColumns(self):
        dataset = self.df.copy()
        return list(dataset.columns)

    def generateHtmlReport(self):
        df = self.df.copy()
        pf = ProfileReport(df, config_file=REPORT_HTML_PATH + 'report_config.yml')
        file_name = 'report_' + datetime.now().strftime('%Y%m%d%H%M%s') + '.html'
        pf.to_file(REPORT_HTML_PATH + file_name)
        return file_name

    def getinfo(self):
        dataset = self.df.copy()
        ans = {}
        ans['correlation'] = self._getCorrectionColumns_(dataset)
        ans['constant'] = self._getConstantColumns_(dataset)
        ans['missing'] = self._getMissingValueColumns_(dataset)
        ans['zero'] = self._getZeroValuesColumns_(dataset)
        ans['columns'] = self._getColumns_(dataset)
        return ans

    def _getColumns_(self, data):
        columns = []
        index = 0
        for column in list(data.columns):
            t = {}
            t['index'] = index
            t['name'] = column
            columns.append(t)
        return columns

    def _getCorrectionColumns_(self, data):
        ans = {}
        for column1 in data:
            for column2 in data:
                if column1 != column2:
                    tmp1 = data[column1].astype('category').cat.codes
                    tmp2 = data[column2].astype('category').cat.codes
                    pearson = tmp1.corr(tmp2)
                    if pearson >= 0.8:
                        ans[pearson] = [column1, column2]

        from collections import defaultdict
        d = defaultdict(list)
        for item in ans.values():
            d[item[0]].append(item[1])

        ans, idx = [], 1
        for key in d:
            tmp = {}
            tmp['index'] = idx
            tmp['columns'] = [key]
            tmp['columns'] += d.get(key)
            ans.append(tmp)
            idx += 1
        return ans

    def _getConstantColumns_(self, data):
        data1 = data.loc[:, (data != data.iloc[0]).any()]
        res = data.columns.difference(data1.columns)
        return list(res)

    def _getMissingValueColumns_(self, data):
        data2 = data.loc[:, (data.isnull()).any()]
        return list(data2.columns)

    def _getZeroValuesColumns_(self, data):
        res = data.count() - data.fillna(0).astype(bool).sum(axis=0)
        res = res.div(4032) * 100
        res = res[res > 10]
        res = res.round(2)
        res = res.sort_values(ascending=False)
        return list(res.index)

    def getColumnProfiling(self, columnName, column_type_dict):
        df = self.df.copy()
        column_df = df[columnName]
        column_type = column_type_dict.get(columnName).get('type')
        column_type_set_by_manual = column_type_dict.get(columnName).get('set_by_manual')
        profiling_result = {}

        # missing value percentage
        profiling_result['missing_value'] = 1 - round(column_df.count() / len(column_df), 2)
        # if this column is empty, return early
        if profiling_result['missing_value'] == 1:
            return profiling_result

        # total count of this column, excluded Nan value
        profiling_result['total'] = str(column_df.count())
        # detect constant column
        self._profiling_column_detect_constant_column_(column_df, profiling_result)
        # if this column is constant, return early
        if 'constant' in profiling_result:
            return profiling_result
        # detect valid percentage
        if column_type_set_by_manual:
            self._profiling_column_detect_valid_percentage_(column_df, profiling_result, column_type)
        else:
            profiling_result['valid'] = 1.0

        if 'int' in column_type or 'float' in column_type:
            self._profiling_numeric_column_(column_df, profiling_result, column_type, column_type_set_by_manual)
        else:
            self._profiling_string_column_(column_df, columnName, profiling_result)



        return profiling_result

    def _profiling_string_column_(self, column_df, column_name, profiling_result):

        # calculate the percentage of uniqueness
        profiling_result['distinct'] = round(len(column_df.unique().tolist()) / len(column_df), 2)
        if profiling_result.get('distinct') != 1.0:
            # top frequency
            profiling_result['top_frequency'] = column_df.mode()[0]
        # extract pattern
        self._profiling_string_column_extract_pattern_(column_df, profiling_result)

    def _profiling_string_column_extract_pattern_(self, column_df, profiling_result):
        patter_extracter = PatternExtracter(list(column_df.dropna()))
        pattern_matchedValue_dict = patter_extracter.determineRegex()
        order_pattern_matchedValue_dict = OrderedDict(
            sorted(pattern_matchedValue_dict.items(), key=lambda t: len(t[1]), reverse=True))

        pattern_ans = []
        count = 0
        for reg, matchedValue in order_pattern_matchedValue_dict.items():
            pattern_ans.append({'pattern': reg.replace('\\', '')[1:-1].replace('[A-Z]', 'word').replace('[0-9]', 'digit').replace('(', '{').replace(')', '}'),
                                'percentage': round(len(matchedValue) / column_df.count() * 100, 2)})
            count += 1
            if count == 3:
                break
        profiling_result['patterns_percentage'] = pattern_ans

    def _profiling_numeric_column_(self, column_df, profiling_result, column_type, set_by_manual):
        column_series = None
        if set_by_manual:
            column_util = ColumnUtil(column_df)
            h = column_util.getColumnTypeHistogram(type=column_type)
            column_series = pd.Series(h.get(column_type)['raw_data'], dtype=np.dtype(column_type))
        else:
            column_series = column_df
        # max
        profiling_result['max'] = float(column_series.max())
        # min
        profiling_result['min'] = float(column_series.min())
        # average
        profiling_result['mean'] = round(column_series.mean(), 2)
        # median
        profiling_result['median'] = column_series.median()
        # count of zero
        profiling_result['zero'] = str(round(int(column_series.where(column_series == 0).count()) / len(column_df) * 100, 2)) + '%'

    def _profiling_column_detect_constant_column_(self, column_df, profiling_result):
        value_frequency_map = column_df.value_counts().to_dict()
        if len(value_frequency_map.keys()) == 1:
            for key, value in value_frequency_map.items():
                profiling_result['constant'] = key

    def _profiling_column_detect_valid_percentage_(self, column_df, profiling_result, column_type):
        if column_type != 'object':
            # valid value percentage
            column_util = ColumnUtil(column_df)
            h = column_util.getColumnTypeHistogram(type=column_type)
            profiling_result['valid'] = h.get(column_type)['count'] / len(column_df)

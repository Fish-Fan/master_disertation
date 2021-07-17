import pandas as pd
from pandas_profiling import ProfileReport
import os
from .. import report_html_location
from datetime import datetime
import json
from app.util.ColumnUtil import ColumnUtil

REPORT_HTML_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), report_html_location)

class Profiling_util:
    def __init__(self, source, data_frame=None):
        self.source = source
        if data_frame:
            self.df = pd.DataFrame(data_frame)
        else:
            self.df = pd.read_csv(self.source)

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
        profiling_result = {}

        columnType = 'string'
        if column_type_dict and columnName in column_type_dict:
            columnType = column_type_dict.get(columnName)

        if columnType in ['int', 'float']:
            profiling_result = self._profiling_numeric_column_(column_df, columnName, columnType)
        else:
            profiling_result = self._profiling_string_column_(column_df, columnName)
        # missing value percentage
        profiling_result['missing_value'] = 1 - column_df.count() / len(column_df)

        if columnType != 'string':
            # valid value percentage
            column_util = ColumnUtil(column_df)
            h = column_util.getColumnTypeHistogram(type=column_type_dict.get(columnName))
            profiling_result['valid'] = h.get(column_type_dict.get(columnName))['count'] / len(column_df)

        return profiling_result

    def _profiling_string_column_(self, column_df, column_name):
        profiling_result = {}
        # calculate the percentage of uniqueness
        profiling_result['distinct'] = len(column_df.unique().tolist()) / len(column_df)
        if profiling_result.get('distinct') != 1.0:
            # top frequency
            profiling_result['top_frequency'] = column_df.mode()[0]
        return profiling_result

    def _profiling_numeric_column_(self, column_df, column_name, columnType ):
        profiling_result = {}
        column_util = ColumnUtil(column_df)
        h = column_util.getColumnTypeHistogram(type=columnType)
        column_series = pd.Series(h.get(columnType)['raw_data'], dtype=columnType)
        # max
        profiling_result['max'] = float(column_series.max())
        # min
        profiling_result['min'] = float(column_series.min())
        # average
        profiling_result['mean'] = column_series.mean()
        # median
        profiling_result['median'] = column_series.median()
        # count of zero
        profiling_result['zero'] = int(column_series.where(column_series == 0).count())
        return profiling_result

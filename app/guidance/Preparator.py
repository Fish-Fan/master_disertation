import pandas as pd
import numpy as np
import re
from app.guidance.DelimiterExtracter import DelimiterExtracter
from app.util.ColumnUtil import ColumnUtil
from collections import defaultdict, OrderedDict
from app.util.ColumnFormatHelper import ColumnFormatHelper
import jsons

class Preparator:
    def __init__(self, name, dataframe, columnIndexMap):
        self.dataframe = dataframe
        self.name = name
        self.columnIndexMap = columnIndexMap

class MarkingResult:
    def  __init__(self, score, column, index, data, description=None):
        self.score = score
        self.column = column
        self.data = data
        self.index = index
        self.description = description
        self.recommend = False

class ListColumnPreparator(Preparator):
    def getColumnList(self):
        column_arr = []
        for key, column in self.columnIndexMap.items():
            column_arr.append(column)
        return column_arr

class DeleteColumnPreparator(Preparator):
    def marking(self):
        markResList = []
        self._getMissingValueColumns_(markResList)
        self._getConstantColumns_(markResList)
        self._getZeroValuesColumns_(markResList)
        return markResList

    def _getMissingValueColumns_(self, markResList):
        df = self.dataframe.copy()
        df1 = df.loc[:, (df.isnull()).any()]
        res = pd.Series(data=len(df1), index=df1.columns) - df1.fillna(0).astype(bool).sum(axis=0)
        res = res.div(len(df1))
        res = res.sort_values(ascending=False)

        d = res.to_dict()
        for key, value in d.items():
            markResList.append(MarkingResult(value, key, self.columnIndexMap.get(key)['index'], None, description='missing'))

    def _getConstantColumns_(self, markResList):
        data = self.dataframe.copy()
        data1 = data.loc[:, (data != data.iloc[0]).any()]
        res = data.columns.difference(data1.columns)

        for column_name in list(res):
            markResList.append(MarkingResult(1.0, column_name, self.columnIndexMap.get(column_name)['index'], None, description='constant'))

    def _getZeroValuesColumns_(self, markResList):
        data = self.dataframe.copy()
        res = data.count() - data.fillna(0).astype(bool).sum(axis=0)
        res = res.div(4032) * 100
        # setting threshold - 80%
        res = res[res > 80]
        res = (res / 100).round(2)
        res = res.sort_values(ascending=False)

        for column_name, score in res.to_dict().items():
            markResList.append(MarkingResult(score, column_name, self.columnIndexMap.get(column_name)['index'], None, description='zero'))

class FillMissingValuePreparator(Preparator):
    def marking(self):
        df = self.dataframe.copy()
        df1 = df.loc[:, (df.isnull()).any()]
        res = pd.Series(data=len(df1), index=df1.columns) - df1.fillna(0).astype(bool).sum(axis=0)
        res = res.div(len(df1))
        res = res.sort_values(ascending=False)
        res = 1 - res

        d = res.to_dict()
        markResList = []

        for column, score in d.items():
            # process empty column
            if len(list(df[column].dropna())) == 0:
                data = {'fillWay': "manual"}
            else:
                column_obj = self.columnIndexMap.get(column)
                column_type = column_obj['type']
                data = {}
                column_util = ColumnUtil(df[column])
                if column_type == 'object':
                    guess_result = column_util.guessColumnType()
                    data = self._construct_column_data_(guess_result.get('type'), guess_result.get('matchValues'),
                                                        column_util)
                else:
                    if column_obj['set_by_manual']:
                        h = column_util.getColumnTypeHistogram(type=column_type)
                        if not h:
                            data = self._construct_column_data_(column_type, h.get(column_type)['raw_data'],
                                                                column_util)
                    else:
                        data = self._construct_column_data_(column_type, list(df[column].dropna()), column_util)
            markResList.append(MarkingResult(score, column, self.columnIndexMap.get(column)['index'], data))
        return markResList

    def _construct_column_data_(self, type, matchedValues, column_util):
        data = {}
        if 'int' in type or 'float' in type:
            data['fillWay'] = 'calculating'
            data['fillMethod'] = 'mean'
            data['fillValue'] = round(
                pd.Series(matchedValues, dtype=np.dtype(type)).mean(), 2)
        else:
            data['fillWay'] = 'calculating'
            data['fillMethod'] = 'frequency'
            data['fillValue'] = column_util.getMostFrequency()
        return data

class SplitColumnPreparator(Preparator):
    def marking(self):
        df = self.dataframe.copy()
        columns = list(df.columns)

        markResList = []
        for column in columns:
            arr = list(df[column].dropna())
            if arr and 'object' == str(df[column].dtype):
                de = DelimiterExtracter(arr)
                de_arr = de.extractDelimiterSet()
                if de_arr:
                    markRes = MarkingResult(de_arr[0]['score'], column, self.columnIndexMap.get(column)['index'], de_arr)
                    markResList.append(markRes)
        return markResList



class ChangeColumnTypePreparator(Preparator):
    def marking(self):
        df = self.dataframe.copy()
        columns = list(df.columns)

        markResList = []
        for column in columns:
            if self.columnIndexMap.get(column)['type'] == 'object':
                column_df = df[column].dropna()
                if len(column_df) > 0:
                    column_util = ColumnUtil(column_df)
                    d = column_util.getColumnTypeHistogram()
                    res = {}
                    res['score'] = 1 - d.get('string')['count'] / len(column_df)
                    # get the most match count
                    for dataType, matched_obj in d.items():
                        if matched_obj['count'] > len(column_df) // 2:
                            res['type'] = dataType
                        else:
                            res['score'] = 0.0
                        break
                    markRes = MarkingResult(res['score'], column, self.columnIndexMap.get(column)['index'],
                                            {'type': res['type']})
                    markResList.append(markRes)
        return markResList



if __name__ == '__main__':
    df = pd.read_csv('../dataset/new_uk_500.csv')
    delete_column_pre = DeleteColumnPreparator('delete_column_pre', df)
    delete_column_res = delete_column_pre.marking()
    print('---delete-column-pre---')
    print(jsons.dumps(delete_column_res))

    print('---fill-missing-value-pre---')
    fill_missing_value_pre = FillMissingValuePreparator('fill_missing_value_pre', df)
    fill_missing_value_ans = fill_missing_value_pre.marking()
    print(jsons.dumps(fill_missing_value_ans))

    print('---split-column-pre---')
    split_column_pre = SplitColumnPreparator('split_column_pre', df)
    split_column_ans = split_column_pre.marking()
    print(jsons.dumps(split_column_ans))

    print('---change-column-type---')
    change_column_pre = ChangeColumnTypePreparator('change_column_pre', df)
    change_column_ans = change_column_pre.marking()
    print(jsons.dumps(change_column_ans))
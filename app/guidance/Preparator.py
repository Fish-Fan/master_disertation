import pandas as pd
import numpy as np
import re
from app.guidance.DelimiterExtracter import DelimiterExtracter
from app.util.ColumnUtil import ColumnUtil
from collections import defaultdict, OrderedDict
import jsons

class Preparator:
    def __init__(self, name, dataframe):
        self.dataframe = dataframe
        self.name = name
        self.columnIndexMap = {}
        for index, col in enumerate(list(self.dataframe.columns)):
            self.columnIndexMap[col] = index

class MarkingResult:
    def  __init__(self, score, column, index, data):
        self.score = score
        self.column = column
        self.data = data
        self.index = index

class ListColumnPreparator(Preparator):
    def getColumnList(self):
        return self.columnIndexMap

class DeleteColumnPreparator(Preparator):
    def marking(self):
        df = self.dataframe.copy()
        df1 = df.loc[:, (df.isnull()).any()]
        res = pd.Series(data=len(df1), index=df1.columns) - df1.fillna(0).astype(bool).sum(axis=0)
        res = res.div(len(df1))
        res = res.sort_values(ascending=False)

        d = res.to_dict()
        markResList = []
        for key, value in d.items():
            markResList.append(MarkingResult(value, key, self.columnIndexMap.get(key),None))
        return markResList

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
            column_util = ColumnUtil(df[column])
            column_type= column_util.guessColumnType()
            data = {}
            if column_type.get('type') in ['int', 'float']:
                data['fillWay'] = 'calculating'
                data['fillMethod'] = 'mean'
                data['fillValue'] = round(pd.Series(column_type.get('matchValues'), dtype=np.dtype(column_type.get('type'))).mean(), 2)
            else:
                data['fillWay'] = 'calculating'
                data['fillMethod'] = 'frequency'
                data['fillValue'] = column_util.getMostFrequency()
            markResList.append(MarkingResult(score, column, self.columnIndexMap.get(column), data))
        return markResList

class SplitColumnPreparator(Preparator):
    def marking(self):
        df = self.dataframe.copy()
        columns = list(df.columns)

        markResList = []
        for column in columns:
            arr = list(df[column].dropna())
            de = DelimiterExtracter(arr)
            delimiter = de.extractBestDelimiter()

            markRes = MarkingResult(delimiter['score'], column, self.columnIndexMap.get(column),{'delimiter': delimiter['delimiter']})
            markResList.append(markRes)
        return markResList



    def _id_to_regex_(self, id):
        x = re.escape(id)
        x = re.sub(r'([^a-zA-Z0-9]+[~+!@#$%^&*./-]*[\s]*)', r'(\1)', x)
        x = re.sub(r'[a-zA-Z]+', r'([A-Z)]+)', x)
        x = re.sub(r'[0-9]+', r'([0-9]+)', x)
        return '^' + x + '$'



class ChangeColumnTypePreparator(Preparator):
    def marking(self):
        df = self.dataframe.copy()
        columns = list(df.columns)

        markResList = []
        for column in columns:
            column_df = df[column].dropna()

            regex_list = {'int': r'^-?\d+$', 'float': r'^\d+.{1}\d+$',
                                    'email': r'^([a-zA-Z0-9._-]+)@([a-zA-Z0-9]+).([a-zA-Z0-9]+)$',
                                    'postal': r'^[A-Z]{1,2}[0-9]{1,2}[A-Z]?\s?[0-9][A-Z]{2}$'}
            d = defaultdict(int)
            d['string'] = 0
            for value in list(column_df):
                count = 0
                for name, reg in regex_list.items():
                    if re.match(reg, str(value)):
                        d[name] += 1
                        count += 1
                if count == 0:
                    d['string'] += 1
            d = OrderedDict(sorted(d.items(), key=lambda t: t[1], reverse=True))
            res = {}
            res['score'] = 1 - d.get('string') / len(column_df)
            # get the most match count
            for key, value in d.items():
                if value > len(column_df) // 2:
                    res['type'] = key
                else:
                    res['score'] = 0.0
                break
            markRes = MarkingResult(res['score'], column, self.columnIndexMap.get(column), {'type': res['type']})
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
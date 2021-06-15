import pandas as pd
class profiling_util:
    def __init__(self, source):
        self.source = source

    def getColumns(self):
        dataset = pd.read_csv(self.source)
        return list(dataset.columns)


    def getinfo(self):
        dataset = pd.read_csv(self.source)
        ans = {}
        ans['correlation'] = self._getCorrectionColumns_(dataset)
        ans['constant'] = self._getConstantColumns_(dataset)
        ans['missing'] = self._getMissingValueColumns_(dataset)
        ans['zero'] = self._getZeroValuesColumns_(dataset)
        return ans

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
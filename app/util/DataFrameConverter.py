import json
import pandas as pd

class DataFrameConverter:
    def __init__(self, df, source):
        if source:
            self.df = pd.read_csv(source)
        else:
            self.df = df



    def doConvert(self, customHeaders=None):
        df = self.df.copy()
        result = df.to_json(orient="records")
        parsed = json.loads(result)
        ans = {}
        ans["tableData"] = parsed
        ans['headers'] = self._getHeaders_(customHeaders=customHeaders)
        return ans


    def _getHeaders_(self, customHeaders=None):
        columns = list(self.df.columns)
        headers = []
        for i, col in enumerate(columns):
            item = {}
            item['prop'] = col
            item['label'] = self._concatenate_headers_(col, customHeaders)
            item['index'] = i
            item['type'] = self._get_column_type_(customHeaders, col)
            headers.append(item)

        return headers

    def _concatenate_headers_(self, label, customHeaders):
        if customHeaders:
            if label in customHeaders:
                return label + ' (' + customHeaders.get(label) + ')'
            else:
                return label + ' (str)'
        else:
            return label + ' (str)'

    def _get_column_type_(self, customHeaders, col):
        if customHeaders and col in customHeaders:
            return customHeaders.get(col)
        else:
            return 'string'



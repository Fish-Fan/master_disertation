import json
import pandas as pd

class DataFrameConverter:
    def __init__(self, df, source):
        if source:
            self.df = pd.read_csv(source)
        else:
            self.df = df



    def doConvert(self):
        df = self.df.copy()
        result = df.to_json(orient="records")
        parsed = json.loads(result)
        ans = {}
        ans["tableData"] = parsed
        ans['headers'] = self._getHeaders_()
        return json.dumps(ans)


    def _getHeaders_(self):
        columns = list(self.df.columns)
        headers = []
        for i, col in enumerate(columns):
            item = {}
            item['prop'] = col
            item['label'] = col
            item['index'] = i
            headers.append(item)

        return headers


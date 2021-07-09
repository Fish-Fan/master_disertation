import pandas as pd
import json
class DataFrameConverter:
    def __init__(self, source):
        self.source = source


    def doConvert(self):
        df = self.source.copy()
        result = df.to_json(orient="records")
        parsed = json.loads(result)
        ans = {}
        ans["code"] = 0
        ans["data"] = parsed
        return json.dumps(ans)


if __name__ == '__main__':
    df = pd.read_csv('../dataset/new_uk_500.csv')
    result = df.to_json(orient="records")
    parsed = json.loads(result)
    ans = {}
    ans["code"] = 0
    ans["data"] = parsed
    print(json.dumps(ans))
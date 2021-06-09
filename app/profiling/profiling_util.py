import pandas as pd
class profiling_util:
    def __init__(self, source):
        self.source = source

    def getColumns(self):
        dataset = pd.read_csv(self.source)
        return list(dataset.columns)
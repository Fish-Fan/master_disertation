import pandas as pd

class ColumnFormatHelper:
    def __init__(self, source, data_frame=None):
        self.source = source
        if source:
            self.df = pd.read_csv(self.source)
        else:
            self.df = data_frame
        self.format_dict = {}

    def get_original_data_format(self):
        tmp_dict = {}
        for column, format in self.df.dtypes.items():
            tmp_dict[column] = str(format)

        for index, col in enumerate(list(self.df.columns)):
            self.format_dict[col] = {'type': tmp_dict.get(col), 'index': index, 'name': col, 'set_by_manual': False}

        return self.format_dict

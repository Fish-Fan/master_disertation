import json
import pandas as pd
from app.util.ColumnFormatHelper import ColumnFormatHelper

class DataFrameConverter:
    def __init__(self, df, source):
        if source:
            self.df = pd.read_csv(source)
        else:
            self.df = df



    def doConvert(self, column_type_dict, isGroupby=False):
        df = self.df.copy()
        ans = {}
        # if it is group by
        if isGroupby:
            ans['isGroupby'] = True
            indexes_type_dict = self._get_indexes_column_type_dict_(list(df.index.names))
            ans['indexes'] = self._getHeaders_(list(df.index.names), indexes_type_dict)
            ans['columns'] = self._getHeaders_(list(df.columns), column_type_dict)
            df = df.reset_index()
        else:
            ans['isGroupby'] = False
            ans['headers'] = self._getHeaders_(list(df.columns), column_type_dict)

        result = df.to_json(orient="records")
        parsed = json.loads(result)

        ans["tableData"] = parsed

        return ans

    def _getHeaders_(self, column_name_list, column_type_dict):
        headers = []
        for i, col in enumerate(column_name_list):
            item = {}
            item['prop'] = col
            item['label'] = self._concatenate_headers_(col, column_type_dict)
            item['index'] = i+1
            item['type'] = column_type_dict[col]['type']
            headers.append(item)

        return headers

    def _concatenate_headers_(self, label, column_type_dict):
        return '{} ({})'.format(label, column_type_dict[label]['type'])

    def _get_indexes_column_type_dict_(self, index_list):
        df_tmp = self.df.reset_index()
        df_tmp = df_tmp.loc[:, index_list]
        cfh = ColumnFormatHelper(None, data_frame=df_tmp)
        return cfh.get_original_data_format()





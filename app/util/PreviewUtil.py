from datetime import datetime
import pandas as pd
import json
from ..util.DataFrameConverter import DataFrameConverter
from flask import session

class PreviewUtil():
    def __init__(self, source):
        self.source = source
        self.df = pd.read_csv(source)

    def getPreviewJson(self, param, session=None):
        deleteObj = param['deleteObj']
        fillingMissingObj = param['fillingMissingObj']
        splittingObj = param['splittingObj']
        changeTypeObj = param['changeTypeObj']

        self._process_delete_operator_(deleteObj)
        self._proces_fill_missing_value_operator_(fillingMissingObj)
        self._process_split_column_operator_(splittingObj)
        session['column_type_dict'] = self._process_change_column_type_operator_(changeTypeObj)
        dfc = DataFrameConverter(self.df, None)
        return dfc.doConvert(customHeaders=session['column_type_dict'])

    def _process_delete_operator_(self, deleteParam):
        columns = deleteParam['columns']
        if columns:
            self.df = self.df.drop(columns, axis=1)

    def _proces_fill_missing_value_operator_(self, fillParam):
        for fillItem in fillParam['columns']:
            column = fillItem['column']
            fillValue = fillItem['fillValue']
            self.df[column] = self.df[column].fillna(fillValue)

    def _process_split_column_operator_(self, splitParam):
        for splitItem in splitParam['columns']:
            column = splitItem['column']
            newColumns = []
            for new_column_item in splitItem['new_column_name_list']:
                newColumns.append(new_column_item['name'])
            delimiter = splitItem['delimiter']
            self.df[newColumns] = self.df[column].str.split(delimiter, expand=True)

    def _process_change_column_type_operator_(self, changeTypeParam):
        columnsType = {}
        for changeTypeItem in changeTypeParam['columns']:
            column = changeTypeItem['column']
            newType = changeTypeItem['data']['type']
            columnsType[column] = newType
        return columnsType





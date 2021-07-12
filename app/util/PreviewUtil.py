from datetime import datetime
import pandas as pd
import json
from ..util.DataFrameConverter import DataFrameConverter
from flask import session

class PreviewUtil():
    def __init__(self, source):
        self.source = source
        self.df = pd.read_csv(source)

    def getPreviewJson(self, param):
        deleteObj = param['deleteObj']
        fillingMissingObj = param['fillingMissingObj']
        # splittingObj = param['splittingObj']
        # changeTypeObj = param['changeTypeObj']

        self._process_delete_operator_(deleteObj)
        self._proces_fill_missing_value_operator_(fillingMissingObj)
        dfc = DataFrameConverter(self.df, None)
        return dfc.doConvert()

    def _process_delete_operator_(self, deleteParam):
        columns = deleteParam['columns']
        if columns:
            self.df = self.df.drop(columns, axis=1)

    def _proces_fill_missing_value_operator_(self, fillParam):
        for fillItem in fillParam['columns']:
            column = fillItem['column']
            fillValue = fillItem['fillValue']
            self.df[column] = self.df[column].fillna(fillValue)



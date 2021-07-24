import pandas as pd
from app.util.ConcatenateDetectionUtil import ConcatenateDetectionUtil
from app.util.JoinDetectionUtil import JoinDetectionUtil
from app.util.ColumnFormatHelper import ColumnFormatHelper

class MultipleFileGuidance:
    def __init__(self, data_frame_1, data_frame_2, data_source_1=None, data_source_2=None):
        self.data_frame_1 = data_frame_1
        self.data_frame_2 = data_frame_2

        if data_source_1:
            self.data_frame_1 = pd.read_csv(data_source_1)
        if data_source_2:
            self.data_frame_2 = pd.read_csv(data_source_2)


    def analysis(self):
        ans = {}
        cdt = ConcatenateDetectionUtil(self.data_frame_1, self.data_frame_2)
        concatenate_result = cdt.marking()

        jdt = JoinDetectionUtil(self.data_frame_1, self.data_frame_2)
        join_result = jdt.marking()

        ans['concatenate_result'] = concatenate_result
        ans['join_result'] = join_result
        ans['concatenate_columns'] = self._get_dataset_column_type_(self.data_frame_2)
        return ans

    def _get_dataset_column_type_(self, df):
        cfh = ColumnFormatHelper(None, data_frame=df)
        return cfh.get_original_data_format()

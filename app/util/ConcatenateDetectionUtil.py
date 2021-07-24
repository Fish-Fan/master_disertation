from app.profiling.Profiling_util import Profiling_util
from app.util.ColumnFormatHelper import ColumnFormatHelper
import pandas as pd
from difflib import SequenceMatcher
from collections import defaultdict

class MarkingResult:
    def __init__(self):
        self.first_score = 0
        self.second_score = 0
        self.third_score = 0



class ConcatenateDetectionUtil:
    def __init__(self, df1, df2):
        self.df1 = df1
        self.df2 = df2


    def marking(self):
        # remove non string columns
        self._drop_non_string_columns_()
        # trying to match columns
        return self._match_columns_()

    def _match_columns_(self):
        pattern_df1 = self._extract_patterns_for_each_column_(self.df1)
        pattern_df2 = self._extract_patterns_for_each_column_(self.df2)

        # pre-process percentage list
        self._pre_process_percentage_(pattern_df1)
        self._pre_process_percentage_(pattern_df2)

        matched_column_result = {}

        tuple_marking_result_dict = defaultdict(list)
        for column_name, column_profiling_result in pattern_df1.items():

            pattern_percentage_list = column_profiling_result['patterns_percentage']
            self._computeScoresForEachColumn_(tuple_marking_result_dict, pattern_percentage_list, pattern_df2, column_name)

        # remove duplicate in tuple_marking_result_dict
        tuple_marking_result_dict = self._remove_duplicate_in_tuple_marking_result_dict_(tuple_marking_result_dict)
        # compute each tuple score
        tuple_marking_result_dict = self._compute_tuple_score_(tuple_marking_result_dict)
        # get the best matched column
        best_matched_result_with_score = self._get_best_matched_column_(tuple_marking_result_dict)
        return best_matched_result_with_score

    def _get_best_matched_column_(self, tuple_marking_result_dict):
        # split via first tuple value
        ans = {}
        for columns_tuple, score in tuple_marking_result_dict.items():
            target_column, matched_column = columns_tuple[0], columns_tuple[1]
            if target_column in ans:
                matched_obj = ans[target_column]
                if matched_obj['score'] < score:
                    matched_obj['matched_column'] = matched_column
                    matched_obj['score'] = score
            else:
                ans[target_column] = {'matched_column': matched_column, 'score': score}
        return ans



    def _compute_tuple_score_(self, tuple_marking_result_dict):
        ans = {}
        for columns_tuple, score_arr in tuple_marking_result_dict.items():
            ans[columns_tuple] = sum(score_arr)
        return ans

    def _remove_duplicate_in_tuple_marking_result_dict_(self, tuple_marking_result_dict):
        ans = {}
        for columns_tuple, score_arr in tuple_marking_result_dict.items():
            t1, t2 = columns_tuple, (columns_tuple[1], columns_tuple[0])
            if t1 not in ans and t2 not in ans:
                ans[t1] = score_arr
        return ans

    def _pre_process_percentage_(self, pattern_df):
        for column_name, column_profiling_result in pattern_df.items():
            pattern_percentage_list = column_profiling_result['patterns_percentage']
            total_percentage = 0
            for pattern_percentage in pattern_percentage_list:
                total_percentage += pattern_percentage['percentage']

            for pattern_percentage in pattern_percentage_list:
                pattern_percentage['percentage'] = pattern_percentage['percentage'] / total_percentage * 100

    def _computeScoresForEachColumn_(self, tuple_marking_result_dict, pattern_percentage_list_1, pattern_df2, column_name_1):

        for i, pattern_percentage_item_1 in enumerate(pattern_percentage_list_1):
            pattern_1 = pattern_percentage_item_1['pattern']
            percentage_1 = pattern_percentage_item_1['percentage']

            for column_name_2, column_profiling_result in pattern_df2.items():
                pattern_percentage_list_2 = column_profiling_result['patterns_percentage']
                if len(pattern_percentage_list_2) > i:
                    pattern_2 = pattern_percentage_list_2[i]['pattern']
                    percentage_2 = pattern_percentage_list_2[i]['percentage']
                    score = self._similiar_(pattern_1, pattern_2) * (percentage_1 + percentage_2) / 2
                    tuple_marking_result_dict[(column_name_1, column_name_2)].append(score)



    def _drop_non_string_columns_(self):
        cfh = ColumnFormatHelper(None, data_frame=self.df1)
        format_df1 = cfh.get_original_data_format()
        cfh = ColumnFormatHelper(None, data_frame=self.df2)
        format_df2 = cfh.get_original_data_format()

        non_string_columns_df1 = []
        non_string_columns_df2 = []

        for column_name, column_obj in format_df1.items():
            if column_obj['type'] == 'object' or 'str' in column_obj['type']:
                continue
            else:
                non_string_columns_df1.append(column_name)

        for column_name, column_obj in format_df2.items():
            if column_obj['type'] == 'object' or 'str' in column_obj['type']:
                continue
            else:
                non_string_columns_df2.append(column_name)

        self.df1 = self.df1.drop(non_string_columns_df1, axis=1)
        self.df2 = self.df2.drop(non_string_columns_df2, axis=1)

    def _extract_patterns_for_each_column_(self, df):
        column_names = list(df.columns)
        ans = {}
        for column_name in column_names:
            pu = Profiling_util(None, data_frame=df)
            profiling_result = {}
            pu._profiling_string_column_(df[column_name], column_name, profiling_result)
            ans[column_name] = profiling_result
        return ans


    def _similiar_(self, a, b):
        return SequenceMatcher(None, a, b).ratio()


if __name__ == '__main__':
    df1 = pd.read_csv('../dataset/Country.csv')
    df2 = pd.read_csv('../dataset/City.csv')

    cdu = ConcatenateDetectionUtil(df1, df2)
    ans = cdu.marking()

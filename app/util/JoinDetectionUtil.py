import pandas as pd
from collections import OrderedDict

class JoinDetectionUtil:
    def __init__(self, df1, df2):
        self.df1 = df1
        self.df2 = df2

    def marking(self):
        # get unique key of each column
        unique_key_df1 = self.getUniqueValueOfEachColumn(self.df1)
        unique_key_df2 = self.getUniqueValueOfEachColumn(self.df2)

        # trying to match different columns
        tuple_marking_result_dict = self.match_columns(unique_key_df1, unique_key_df2)
        # get the best match result
        best_join_keys_with_score = self.get_best_matched_column(tuple_marking_result_dict)
        print('111')

    def get_best_matched_column(self, tuple_marking_result_dict):
        d = OrderedDict(sorted(tuple_marking_result_dict.items(), key=lambda t: t[1], reverse=True))
        for column_tuple, score in d.items():
            return {'join_keys': column_tuple, 'score': score}

    def match_columns(self, unique_key_df1, unique_key_df2):
        tuple_marking_result_dict = {}
        for column_name_1, unique_key_series_1 in unique_key_df1.items():
            for column_name_2, unique_key_series_2 in unique_key_df2.items():
                intersection = unique_key_series_1.intersection(unique_key_series_2)
                score = len(intersection) / len(unique_key_series_1) * 100
                tuple_marking_result_dict[(column_name_1, column_name_2)] = score
        return tuple_marking_result_dict


    def getUniqueValueOfEachColumn(self, df):
        column_names = list(df.columns)
        ans = {}

        for column_name in column_names:
            ans[column_name] = df[column_name].value_counts().keys()
        return ans


if __name__ == '__main__':
    df1 = pd.read_csv('../dataset/Country.csv')
    df2 = pd.read_csv('../dataset/City.csv')

    cdu = JoinDetectionUtil(df1, df2)
    cdu.marking()
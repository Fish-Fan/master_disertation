import pandas as pd
import jsons
from app.util.ColumnFormatHelper import ColumnFormatHelper
from collections import defaultdict, OrderedDict
from app.guidance.Preparator import ListColumnPreparator, DeleteColumnPreparator, FillMissingValuePreparator, SplitColumnPreparator, ChangeColumnTypePreparator
from app.util.ElaspeDecorator import elapse_decorator

class Guidance:
    def __init__(self, source, columnTypeMap, data_frame=None):
        self.source = source
        if source:
            self.df = pd.read_csv(self.source)
        else:
            self.df = data_frame
        self.columnTypeMap = columnTypeMap

    def analysis(self):
        ans = {}
        list_column_pre = ListColumnPreparator('list_column_pre', self.df, self.columnTypeMap)
        ans['list_column_pre'] = list_column_pre.getColumnList()

        delete_column_pre = DeleteColumnPreparator('delete_column_pre', self.df, self.columnTypeMap)
        ans['delete_column_pre'] = delete_column_pre.marking()


        fill_missing_value_pre = FillMissingValuePreparator('fill_missing_value_pre', self.df, self.columnTypeMap)
        ans['fill_missing_value_pre'] = fill_missing_value_pre.marking()

        change_column_pre = ChangeColumnTypePreparator('change_column_pre', self.df, self.columnTypeMap)
        ans['change_column_type_pre'] = change_column_pre.marking()

        self.score_based_algorithm(ans)
        return ans

    # in order to improve application performance, separate this method out from analysis
    def split_column_guidance(self):
        split_column_pre = SplitColumnPreparator('split_column_pre', self.df, self.columnTypeMap)
        return split_column_pre.marking()


    def score_based_algorithm(self, preparator_collection):
        column_operation_dict = defaultdict(list)
        for preparator, column_obj_collection in preparator_collection.items():
            if preparator != 'list_column_pre':
                for column_obj in column_obj_collection:
                    column_name = column_obj.column
                    column_operation_dict[column_name].append(column_obj)
        for column_name, column_operation_collection in column_operation_dict.items():
            column_operation_dict[column_name] = sorted(column_operation_collection, key=lambda x:x.score, reverse=True)

        # for each column only suggest one type operation
        for column_name, column_operation_collection in column_operation_dict.items():
            if len(column_operation_collection) > 0:
                column_operation_collection[0].recommend = True


if __name__ == '__main__':
    source = '../dataset/new_uk_500.csv'
    g = Guidance(source)
    ans = g.analysis()
    print(ans)
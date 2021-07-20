import pandas as pd
import jsons
from app.util.ColumnFormatHelper import ColumnFormatHelper
from app.guidance.Preparator import ListColumnPreparator, DeleteColumnPreparator, FillMissingValuePreparator, SplitColumnPreparator, ChangeColumnTypePreparator
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

        split_column_pre = SplitColumnPreparator('split_column_pre', self.df, self.columnTypeMap)
        ans['split_column_pre'] = split_column_pre.marking()

        change_column_pre = ChangeColumnTypePreparator('change_column_pre', self.df, self.columnTypeMap)
        ans['change_column_type_pre'] = change_column_pre.marking()

        return ans

if __name__ == '__main__':
    source = '../dataset/new_uk_500.csv'
    g = Guidance(source)
    ans = g.analysis()
    print(ans)
import pandas as pd
import jsons
from app.guidance.Preparator import ListColumnPreparator, DeleteColumnPreparator, FillMissingValuePreparator, SplitColumnPreparator, ChangeColumnTypePreparator
class Guidance:
    def __init__(self, source):
        self.source = source

    def analysis(self):
        ans = {}
        df = pd.read_csv(self.source)
        list_column_pre = ListColumnPreparator('list_column_pre', df)
        ans['list_column_pre'] = list_column_pre.getColumnList()

        delete_column_pre = DeleteColumnPreparator('delete_column_pre', df)
        ans['delete_column_pre'] = delete_column_pre.marking()


        fill_missing_value_pre = FillMissingValuePreparator('fill_missing_value_pre', df)
        ans['fill_missing_value_pre'] = fill_missing_value_pre.marking()

        split_column_pre = SplitColumnPreparator('split_column_pre', df)
        ans['split_column_pre'] = split_column_pre.marking()

        change_column_pre = ChangeColumnTypePreparator('change_column_pre', df)
        ans['change_column_type_pre'] = change_column_pre.marking()

        return jsons.dumps(ans)

if __name__ == '__main__':
    source = '../dataset/new_uk_500.csv'
    g = Guidance(source)
    ans = g.analysis()
    print(ans)
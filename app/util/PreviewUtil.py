from datetime import datetime
import pandas as pd
import numpy as np
import jsons
from app.util.DataFrameConverter import DataFrameConverter
from flask import session
from app.util.ColumnFormatHelper import ColumnFormatHelper
from app.guidance.Guidance import Guidance

class PreviewUtil():
    def __init__(self, source):
        self.source = source
        self.df = pd.read_csv(source)


    def getPreviewJson(self, param, session):
        recipe_list = param['recipe_list']
        column_new_type_dict = {}
        is_group_by = False
        for step in recipe_list:
            if step['type'] == 'deleteColumn':
                self._process_delete_operator_(step['data'])
            elif step['type'] == 'fillMissingValue':
                self._proces_fill_missing_value_operator_(step['data'])
            elif step['type'] == 'splittingColumnValue':
                self._process_split_column_operator_(step['data'])
            elif step['type'] == 'changeColumnType':
                self._process_change_column_type_operator_(step['data'], column_new_type_dict)
            elif step['type'] == 'queryBuilder':
                self._process_query_bulider_operator_(step['data'])
            elif step['type'] == 'groupby':
                is_group_by = self._process_groupby_operator_(step['data'])

        ans = {}
        # update column type before doing analysis
        column_type_dict = self._get_updated_column_type_dict_(column_new_type_dict)
        dfc = DataFrameConverter(self.df, None)
        ans['preview_dataset'] = dfc.doConvert(column_type_dict, isGroupby=is_group_by)
        session['column_type_dict'] = column_type_dict
        g = Guidance(None, column_type_dict ,data_frame=self.df)
        ans['profiling_result'] = g.analysis()
        return jsons.dumps(ans)

    def _get_updated_column_type_dict_(self, column_new_type_dict):
        cfh = ColumnFormatHelper(None, data_frame=self.df)
        column_type_dict = cfh.get_original_data_format()
        for column_name, column_obj in column_type_dict.items():
            if column_name in column_new_type_dict:
                column_obj['type'] = column_new_type_dict.get(column_name)
                column_obj['set_by_manual'] = True
                if column_obj['type'] == 'category':
                    column_obj['categories'] = list(self.df[column_name].value_counts().keys())

        return column_type_dict


    def _process_delete_operator_(self, deleteParam):
        if deleteParam:
            self.df = self.df.drop(deleteParam, axis=1)

    def _proces_fill_missing_value_operator_(self, fillItem):
        column = fillItem['column']
        fillValue = fillItem['fillValue']
        self.df[column] = self.df[column].fillna(fillValue)


    def _process_split_column_operator_(self, splitItem):
        column = splitItem['column']
        newColumns = []
        for new_column_item in splitItem['new_column_name_list']:
            newColumns.append(new_column_item['name'])
        delimiter = splitItem['delimiter']
        self.df[newColumns] = self.df[column].str.split(delimiter, expand=True)


    def _process_change_column_type_operator_(self, changeTypeItem, column_new_type_dict):
        column = changeTypeItem['column']
        newType = changeTypeItem['data']['type']
        column_new_type_dict[column] = newType
        # self._do_change_column_type_(column, newType)


    # def _do_change_column_type_(self, column_name, column_type):
    #     regex_list = {'int': r'^-?\d+$', 'float': r'^\d+.{1}\d+$',
    #                   'email': r'^([a-zA-Z0-9._-]+)@([a-zA-Z0-9]+).([a-zA-Z0-9]+)([.uk]*)$',
    #                   'postal': r'^[A-Z]{1,2}[0-9]{1,2}[A-Z]?\s?[0-9][A-Z]{2}$'}
    #     regx = regex_list.get(column_type)
    #
    #     self.df = self.df[self.df[column_name].notnull() & self.df[column_name].str.match(regx)]
    #     # change column type
    #     if column_type in ['int', 'float']:
    #         self.df[column_name] = self.df[column_name].astype(column_type)
    #     else:
    #         self.df[column_name] = self.df[column_name].astype('string')

    def _process_query_bulider_operator_(self, queryBuilderParam):
        match_type = queryBuilderParam['matchType']
        filter_list = queryBuilderParam['filterList']
        expression = ""
        expression_string_pattern = '{}.notnull() and {}.str.{}("{}") {} '
        expression_num_pattern = '{} {} {} {} '
        for index, filter_item in enumerate(filter_list):
            if filter_item['operator'] == 'contains':
                expression += expression_string_pattern.format(filter_item['name'], filter_item['name'], 'contains', filter_item['value'], match_type)
            elif filter_item['operator'] == 'equals':
                expression += '{} {} "{}" {} '.format(filter_item['name'], '==', filter_item['value'], match_type)
            elif filter_item['operator'] == 'begin with':
                expression += expression_string_pattern.format(filter_item['name'], filter_item['name'], 'startswith', filter_item['value'], match_type)
            elif filter_item['operator'] == 'end with':
                expression += expression_string_pattern.format(filter_item['name'], filter_item['name'], 'endswith', filter_item['value'],
                                                               match_type)
            elif filter_item['operator'] == 'is empty':
                expression += "{}.{} {} ".format(filter_item['name'], 'isnull()', match_type)
            elif filter_item['operator'] == 'is not empty':
                expression += '{}.{} {} '.format(filter_item['name'], 'notnull()', match_type)
            elif filter_item['operator'] == 'greater than':
                expression += expression_num_pattern.format(filter_item['name'], '>', filter_item['value'], match_type)
            elif filter_item['operator'] == 'less than':
                expression += expression_num_pattern.format(filter_item['name'], '<', filter_item['value'], match_type)
            elif filter_item['operator'] == 'less and equal than':
                expression += expression_num_pattern.format(filter_item['name'], '<=', filter_item['value'], match_type)
            elif filter_item['operator'] == 'greater and equal than':
                expression += expression_num_pattern.format(filter_item['name'], '>=', filter_item['value'], match_type)

        if match_type == 'and':
            expression = expression[:len(expression)-4]
        elif match_type == 'or':
            expression = expression[:len(expression)-3]

        num_columns = []
        for filter_item in filter_list:
            if filter_item['type'] in ['int', 'float']:
                num_columns.append({'name': filter_item['name'], 'type': filter_item['type']})

        # pre process dataset
        self.df = self.df.query(expression)

    def _process_groupby_operator_(self, groupbyParam):
        splitters = groupbyParam['splitters']
        column_aggregations = groupbyParam['column_aggregations']

        agg_dict = {}
        for column_aggregation_item in column_aggregations:
            agg_dict[column_aggregation_item['column']] = column_aggregation_item['aggre_funcs']

        self.df = self.df.groupby(splitters).agg(agg_dict)

        new_column_names = []
        for column_name, aggregation_funcs in agg_dict.items():
            for aggregation_func_name in aggregation_funcs:
                new_column_names.append('{}_{}'.format(column_name, aggregation_func_name))
        self.df.columns = new_column_names

        return True



if __name__ == '__main__':
    pu = PreviewUtil('../dataset/new_uk_500.csv')
    param = {
        'matchType': 'and',
        'filterList': [{
            'index': 0,
            'name': 'name',
            'operator': 'is not empty',
            'type': 'string'
        }]
    }
    pu._process_query_bulider_operator_(param)
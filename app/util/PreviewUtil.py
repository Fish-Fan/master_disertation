from datetime import datetime
import pandas as pd
import numpy as np
import jsons
from app.util.DataFrameConverter import DataFrameConverter
from flask import session
from app.util.ColumnFormatHelper import ColumnFormatHelper
from app.guidance.Guidance import Guidance
from collections import OrderedDict
from app.util.ElaspeDecorator import elapse_decorator

class PreviewUtil():
    def __init__(self, source, data_path):
        self.source = source
        self.source_name = source.split('/')[-1][:-4]
        self.df = pd.read_csv(source)
        self.data_path = data_path
        # for multiple files data wrangling use
        self.wrangling_index = 0

    @elapse_decorator
    def getPreviewJson(self, param, session):
        recipe_list = param['recipe_list']
        column_new_type_dict = {}
        is_group_by = False
        for step in recipe_list:
            if step['type'] == 'DeleteColumn':
                self._process_delete_operator_(step['data'])
            elif step['type'] == 'FillMissingValue':
                self._proces_fill_missing_value_operator_(step['data'])
            elif step['type'] == 'SplittingColumnValue':
                self._process_split_column_operator_(step['data'])
            elif step['type'] == 'ChangeColumnType':
                self._process_change_column_type_operator_(step['data'], column_new_type_dict)
            elif step['type'] == 'Filter':
                self._process_query_bulider_operator_(step['data'])
            elif step['type'] == 'Aggregation':
                is_group_by = self._process_groupby_operator_(step['data'])
            elif step['type'] == 'concat':
                self._process_concat_operator_(step['data'], session)
            elif step['type'] == 'join':
                self._process_join_operator_(step['data'], session)

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

    @elapse_decorator
    def _process_delete_operator_(self, deleteParam):
        if deleteParam:
            self.df = self.df.drop(deleteParam, axis=1)

    @elapse_decorator
    def _proces_fill_missing_value_operator_(self, fillItem):
        column = fillItem['column']
        fillValue = fillItem['fillValue']
        self.df[column] = self.df[column].fillna(fillValue)

    @elapse_decorator
    def _process_split_column_operator_(self, splitItem):
        column = splitItem['column']
        newColumns = []
        for new_column_item in splitItem['new_column_name_list']:
            newColumns.append(new_column_item['name'])
        delimiter = splitItem['delimiter']
        self.df[newColumns] = self.df[column].str.split(delimiter, expand=True)

    @elapse_decorator
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

    @elapse_decorator
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
        # TODO hard code join type, should be flexible in later version
        if match_type == 'and':
            expression = expression[:len(expression)-5]
        else:
            expression = expression[:len(expression)-4]

        num_columns = []
        for filter_item in filter_list:
            if filter_item['type'] in ['int', 'float']:
                num_columns.append({'name': filter_item['name'], 'type': filter_item['type']})

        # pre process dataset
        self.df = self.df.query(expression)

    @elapse_decorator
    def _process_groupby_operator_(self, groupbyParam):
        splitters = groupbyParam['splitters']
        column_aggregations = groupbyParam['column_aggregations']

        agg_dict = {}
        for column_aggregation_item in column_aggregations:
            # identify count(distinct)
            if 'count(distinct)' in column_aggregation_item['aggre_funcs']:
                agg_dict[column_aggregation_item['column']] = [pd.Series.nunique if x == 'count(distinct)' else x for x in column_aggregation_item['aggre_funcs']]
            else:
                agg_dict[column_aggregation_item['column']] = column_aggregation_item['aggre_funcs']

        self.df = self.df.groupby(splitters).agg(agg_dict)

        new_column_names = []
        for column_name, aggregation_funcs in agg_dict.items():
            for aggregation_func_name in aggregation_funcs:
                if aggregation_func_name == pd.Series.nunique:
                    new_column_names.append('{}_{}'.format(column_name, 'count(distinct)'))
                else:
                    new_column_names.append('{}_{}'.format(column_name, aggregation_func_name))
        self.df.columns = new_column_names

        return True

    @elapse_decorator
    def _process_concat_operator_(self, concatParam, session):
        new_column_name_list = concatParam
        new_df_obj = self._get_new_df_from_session_(session)
        new_wrangling_df = new_df_obj['data_frame']
        new_wrangling_file_name = new_df_obj['file_name']
        # iterate new_column_name_list and rename its column, prepare for concatenation
        cfh = ColumnFormatHelper(None, data_frame=new_wrangling_df)
        format_dict = cfh.get_original_data_format()
        for new_column_obj in new_column_name_list:
            origin_name = new_column_obj['origin_name']
            new_name = new_column_obj['new_name']
            format_dict[new_name] = format_dict.pop(origin_name)

        d = OrderedDict(sorted(format_dict.items(), key=lambda t: t[1]['index']))

        # do change column name
        new_wrangling_df.columns = d.keys()
        self.df = pd.concat([self.df, new_wrangling_df], ignore_index=True, sort=False)

    @elapse_decorator
    def _process_join_operator_(self, joinParam, session):
        new_df_obj = self._get_new_df_from_session_(session)
        new_wrangling_df = new_df_obj['data_frame']
        left_dataset_name = self.source_name
        right_dataset_name = new_df_obj['file_name']
        left_on = joinParam['left_on']
        right_on = joinParam['right_on']
        self.df = pd.merge(self.df, new_wrangling_df, how="left", left_on=left_on, right_on=right_on, suffixes=('' , '_' + right_dataset_name))


    def _get_new_df_from_session_(self, session):
        new_wrangling_file_name = session['wrangling_files'][self.wrangling_index]
        ans =  {
            'data_frame': pd.read_csv(self.data_path + new_wrangling_file_name),
            'file_name': session['wrangling_files'][self.wrangling_index][:-4]
        }
        self.wrangling_index += 1
        return ans

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
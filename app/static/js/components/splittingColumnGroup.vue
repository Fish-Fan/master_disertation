<template>
    <el-tabs v-model="activeTab" tab-position="top">
        <el-tab-pane
                v-for="column_item_obj in submitSplitColumns"
                :key="'splitting-tab-' + column_item_obj.index "
                :name="column_item_obj.column"
                >
            <span slot="label"><i v-if="column_item_obj.recommend" class="el-icon-star-on"></i> {{column_item_obj.column}}</span>
            <el-form ref="form" :model="column_item_obj.form">
                <el-form-item label="choose your delimiter">
                    <el-select v-model="column_item_obj.form.submit.delimiter" placeholder="select" @change="handleDelimiterChangeEvent(column_item_obj.form)">
                        <el-option
                          v-for="(delimiterItem, index) in column_item_obj.form.delimiter_obj_list"
                          :key="index"
                          :label="computeDisplayDelimiter(delimiterItem.delimiter)"
                          :value="delimiterItem.delimiter">
                        </el-option>
                    </el-select>
                </el-form-item>
                <el-form-item v-for="(new_column_item, index) in column_item_obj.form.submit.new_column_name_list" :label="computeLabel(index)">
                    <el-input v-model="new_column_item.name"></el-input>
                </el-form-item>

                <el-form-item>
                    <el-button type="success" @click="addRecipe(column_item_obj.form.submit)" size="mini" plain >Add Recipe</el-button>
                </el-form-item>
            </el-form>
        </el-tab-pane>
    </el-tabs>
</template>

<script>
  module.exports = {
    props: ['column_list'],
    methods: {
        computeSubmitSplitColumns: function() {
            var submitSplitColumns = [];
            for (column_item of this.column_list) {
                var column_item_obj = {};
                column_item_obj.column = column_item.column;
                column_item_obj.index = column_item.index;
                column_item_obj.score = column_item.score;
                column_item_obj.recommend = column_item.recommend;

                column_item_obj.form = {};
                column_item_obj.form.delimiter_obj_list = [];
                for (data_item of column_item.data) {
                    var delimiter_obj = {};
                    delimiter_obj.delimiter = data_item.delimiter;
                    delimiter_obj.max_count = data_item.max_count;
                    column_item_obj.form.delimiter_obj_list.push(delimiter_obj);
                }

                var submit = {};
                submit.delimiter = column_item_obj.form.delimiter_obj_list[0].delimiter;
                var newColumnNameList = [];
                for (let i = 0; i < column_item_obj.form.delimiter_obj_list[0].max_count; i++) {
                    newColumnNameList.push({name: ''});
                }
                submit.new_column_name_list = newColumnNameList;
                column_item_obj.form.submit = submit;

                submitSplitColumns.push(column_item_obj)
            }

            return submitSplitColumns;
        },
        handleDelimiterChangeEvent(form) {
            form.submit.new_column_name_list = this.computedDelimiterNewColumnNames(form);
        },
        computedDelimiterOptions: function(form) {
            var delimiter_obj_list = form.delimiter_obj_list;
            var delimiterOptions = [];
            for (item of delimiter_obj_list) {
                delimiterOptions.push(item.delimiter);
            }
            return delimiterOptions;
        },
        computedDelimiterNewColumnNames: function(form) {
            var delimiter = form.submit.delimiter;
            var maxCount = 0;
            for (item of form.delimiter_obj_list) {
                if (item.delimiter == delimiter) {
                    maxCount = item.max_count;
                }
            }
            var delimiterOptions = [];
            for (let i = 0; i < maxCount; i++) {
                delimiterOptions.push({name: ''});
            }
            return delimiterOptions;
        },
        computeLabel: function(index) {
            return 'input your ' + (index + 1) + ' column name after splitting'
        },
        computeDisplayDelimiter: function(delimiter) {
            if (delimiter.replace(/\s/g, '').length == 0) {
                return delimiter.length + ' blank space'
            } else {
                return delimiter
            }
        },
        addRecipe: function(submitObj) {
            submitObj.column = this.activeTab;
            splittingColumnRecipe = {
                type: 'splittingColumnValue',
                description: this.concatenateDescription(submitObj),
                data: submitObj
            };
            this.$emit('split-column-value-recipe-event', splittingColumnRecipe);
        },
        concatenateDescription: function(submitObj) {
            var new_column_name_str = '[';
            for (newColumnObj of submitObj.new_column_name_list) {
                new_column_name_str += newColumnObj.name + ',';
            }
            new_column_name_str = new_column_name_str.substring(0, new_column_name_str.length-1);
             new_column_name_str += ']';
            return 'Using "' + submitObj.delimiter + '" as a delimiter to split ' + submitObj.column + ' into ' + submitObj.new_column_name_list.length + ' parts, new columns names as the following: ' + new_column_name_str;
        }
    },
    computed: {
        computedColumnMap: function() {
            var columnMap = new Map();
            for (column_item_obj of this.submitSplitColumns) {
                columnMap.set(column_item_obj.column, column_item_obj);
                delimiterMap = new Map();
                this.columnMap.set(column_item.column, column_item_obj);
                for (delimiter_obj of column_item_obj.form.delimiter_obj_list) {
                    delimiterMap.set(delimiter_obj.delimiter, delimiter_obj.submitedNewColumnNames);
                }
            }
            return columnMap;
        },
        computedActiveTab: function () {
            if (this.column_list.length != 0) {
                return column_list[0].column;
            }
        }
    },
    watch: {
        column_list: function (newVal, oldVal) {
            if (newVal.length > 0) {
                this.submitSplitColumns = this.computeSubmitSplitColumns(newVal);
                this.activeTab = newVal[0].column;
            }
        }
    },
    data() {
      return {
          submitSplitColumns: [],
          activeTab: '',
          columnMap: {}
      }
    }
  }
</script>
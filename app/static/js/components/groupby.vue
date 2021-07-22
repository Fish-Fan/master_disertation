<template>
  <el-form ref="form" v-loading="loading">
        <label>choose your splitter</label>
        <el-form-item>
            <el-select class="splitter" v-model="spilitter_submit" multiple placeholder="select" size="mini">
                <el-option
                  v-for="(option, index) in category_columns"
                  :key="index"
                  :label="option.name"
                  :value="option.name">
                </el-option>
            </el-select>
            <el-button type="success" @click="addColumn()" size="mini" plain ><i class="el-icon-circle-plus-outline"></i></el-button>
        </el-form-item>
        <label>choose your target columns and aggregation functions</label>
        <el-form-item>
            <div v-for="(column_aggregation_func, column_aggregation_func_index) in column_aggregation_funcs_submit">
                <el-select class="column_aggregation" v-model="column_aggregation_func.column" placeholder="select" size="mini">
                    <el-option
                      v-for="(column, index) in numeric_columns"
                      :key="index"
                      :label="column.name"
                      :value="column.name">
                    </el-option>
                </el-select>
                <el-select class="column_aggregation" v-model="column_aggregation_func.aggre_funcs" multiple placeholder="select" size="mini">
                    <el-option
                      v-for="(function_name, index) in aggregation_functions"
                      :key="index"
                      :label="function_name"
                      :value="function_name">
                    </el-option>
                </el-select>
                <el-button type="error" @click="removeColumn(column_aggregation_func_index)" size="mini" plain ><i class="el-icon-remove-outline"></i></el-button>
            </div>
        </el-form-item>

        <el-button type="success" @click="addRecipe" size="mini" plain>Add Recipe</el-button>
  </el-form>
</template>

<script>
  module.exports = {
    props: ['column_list', 'is_loading'],
    methods: {
        computeNumericAndCategoryColumns(column_list) {
            var numeric_arr = [];
            var category_arr = [];
            for(column_item of column_list) {
                if (column_item.type.includes('int') || column_item.type.includes('float')) {
                    numeric_arr.push(column_item);
                }
                if (column_item.type.includes('category')) {
                    category_arr.push(column_item)
                }
            }
            this.numeric_columns = numeric_arr;
            this.category_columns = category_arr;
        },
        addColumn() {
            this.column_aggregation_funcs_submit.push({
                column: "",
                aggre_funcs: []
            });
        },
        removeColumn(index) {
            this.column_aggregation_funcs_submit.splice(index, 1);
        },
        concatRecipeDescription(splitter_columns, column_aggregations) {
            var split_desc = "splitting data into groups via " + splitter_columns.toString() + " ";
            var group_desc = "";
            for (column_aggregation_item of column_aggregations) {
                group_desc += "group by " + column_aggregation_item.column + " via using " + column_aggregation_item.aggre_funcs.toString() + " functions; "
            }
            return split_desc + group_desc;
        },
        addRecipe() {
            var groupByRecipe = {
                type: 'groupby',
                description: this.concatRecipeDescription(this.spilitter_submit, this.column_aggregation_funcs_submit),
                data: {
                    'splitters': this.spilitter_submit,
                    'column_aggregations': this.column_aggregation_funcs_submit
                }
            };
            this.$emit('group-by-recipe-event', groupByRecipe);
         }
    },
    watch: {
        is_loading: function(newVal, oldVal) {
            this.loading = newVal
        },
        column_list: function(newVal, oldVal) {
            this.computeNumericAndCategoryColumns(newVal);
        }
    },
    data() {
        return {
            spilitter_submit: [],
            column_aggregation_funcs_submit: [],
            numeric_columns: [],
            category_columns: [],
            aggregation_functions: ['max', 'min', 'mean', 'sum'],
            loading: false
        }
    }
  }
</script>
<style>
.column_aggregation{
    width: 40%;
}
.splitter {
    width: 80%;
}
</style>
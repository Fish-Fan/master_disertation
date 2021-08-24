<template>
  <el-form ref="form" v-loading="loading">
        <el-form-item>
            <el-select v-model="query.matchType" placeholder="select" size="mini">
                <el-option
                  v-for="(option, index) in matchType"
                  :key="index"
                  :label="option"
                  :value="option">
                </el-option>
            </el-select>

            <el-select v-model="addColumn" placeholder="select" size="mini">
                <el-option
                  v-for="column in column_list"
                  :key="column.index"
                  :label="column.name"
                  :value="column.name">
                </el-option>
            </el-select>

            <el-button type="success" @click="addRule()" size="mini" plain >Add Rule</el-button>
        </el-form-item>
        <el-form-item v-for="(column, index) in query.filterList">
            <label>{{ column.name }}</label>
            <div v-if="column.type === 'category'">
                <el-select v-model="column.operator" placeholder="select" size="mini" @change="categoryOperatorChange(column)">
                    <el-option
                      v-for="(operator, index) in stringOperators"
                      :key="index"
                      :label="operator"
                      :value="operator">
                    </el-option>
                </el-select>
                <el-select v-model="column.value" placeholder="select" size="mini" :disabled="column.disabled">
                    <el-option
                      v-for="(category_item, index) in column.categories"
                      :key="index"
                      :label="category_item"
                      :value="category_item">
                    </el-option>
                </el-select>
                <el-button size="mini" icon="el-icon-remove" @click="handleRemoveButton(index)"></el-button>
            </div>
            <el-input v-else v-model="column.value" class="input-with-select" size="mini" :disabled="column.disabled">
                <el-select style="width: 150px" v-if="column.type.includes('int') || column.type.includes('float')" v-model="column.operator" placeholder="select" size="mini" slot="prepend" @change="operatorChange(column)">
                    <el-option
                      v-for="(operator, index) in numberOperators"
                      :key="index"
                      :label="operator"
                      :value="operator">
                    </el-option>
                </el-select>
                <el-select style="width: 150px" v-else v-model="column.operator" placeholder="select" size="mini" slot="prepend" @change="operatorChange(column)">
                    <el-option
                      v-for="(operator, index) in stringOperators"
                      :key="index"
                      :label="operator"
                      :value="operator">
                    </el-option>
                </el-select>
                <el-button slot="append" icon="el-icon-remove" @click="handleRemoveButton(index)"></el-button>
            </el-input>
        </el-form-item>

        <el-button type="success" @click="addRecipe" size="mini" plain>Add Recipe</el-button>
  </el-form>
</template>

<script>
  module.exports = {
    props: ['column_list', 'is_loading'],
    methods: {
        categoryOperatorChange(column) {
            if (column.operator == 'is empty' || column.operator == 'is not empty') {
                column.disabled = true;
                column.value = "";
            } else {
                column.disabled = false;
            }
        },
        operatorChange(column) {
            if (column.operator == 'is empty' || column.operator == 'is not empty') {
                column.disabled = true
            } else {
                column.disabled = false
            }
        },
        computeValueInputDisable(value) {
            return value
        },
        concatRecipeDescription(filterList) {
            var condition = "dataset.query( ";
            for (filter_item of filterList) {
                condition += filter_item.name + " " + filter_item.operator + " " + filter_item.value + " " + this.query.matchType + " ";
            }
            condition = condition.substring(0, condition.length - 4);
            condition += " )";
            return condition;
        },
        addRecipe() {
            var queryBuilderRecipe = {
                type: 'Filter',
                description: this.concatRecipeDescription(this.query.filterList),
                data: this.query,
                guidance_category: 'filter'
            };
            this.$emit('query-builder-recipe-event', queryBuilderRecipe);
         },
        addRule () {
            for (column_item of this.column_list) {
                if (this.addColumn == column_item.name) {
                    var new_column_item = {};
                    new_column_item.disabled = false;
                    new_column_item.index = column_item.index;
                    new_column_item.name = column_item.name;
                    new_column_item.operators = column_item.operators;
                    new_column_item.set_by_manual = column_item.set_by_manual;
                    new_column_item.type = column_item.type;
                    new_column_item.value = "";
                    this.query.filterList.push(new_column_item);
                }
            }
        },
        handleRemoveButton(index) {
            this.query.filterList.splice(index, 1);
        }
    },
    watch: {
        is_loading: function(newVal, oldVal) {
            this.loading = newVal
        }
    },
    data() {
        return {
            query: {
                matchType: "",
                filterList: [

                ]
            },
            matchType: ["and", "or "],
            addColumn: "",
            stringOperators: ["equals", "contains", "begin with", "end with", "is empty", "is not empty"],
            numberOperators: ["equals", "greater than", "less than", "less and equal than", "greater and equal than"],
            loading: false
        }
    }
  }
</script>
<style>
  .input-with-select .el-input-group__prepend {
    background-color: #fff;
  }
</style>
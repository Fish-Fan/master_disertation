<template>
  <el-form ref="form">
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
            <el-input v-model="column.value" class="input-with-select" size="mini" :disabled="column.disabled">
                <el-select v-if="column.type === 'int' || column.type === 'float'" v-model="column.operator" placeholder="select" size="mini" slot="prepend" @change="operatorChange(column)">
                    <el-option
                      v-for="(operator, index) in numberOperators"
                      :key="index"
                      :label="operator"
                      :value="operator">
                    </el-option>
                </el-select>
                <el-select v-else v-model="column.operator" placeholder="select" size="mini" slot="prepend" @change="operatorChange(column)">
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
    props: ['column_list'],
    methods: {
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
                type: 'queryBuilder',
                description: this.concatRecipeDescription(this.query.filterList),
                data: this.query
            };
            this.$emit('query-builder-recipe-event', queryBuilderRecipe);
         },
        addRule () {
            for (column_item of this.column_list) {
                if (this.addColumn == column_item.name) {
                    column_item.disabled = false;
                    this.query.filterList.push(column_item);
                }
            }
        },
        handleRemoveButton(index) {
            this.query.filterList.splice(index, 1);
        }
    },
    watch: {

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
            numberOperators: ["equals", "greater than", "less than", "less and equal than", "greater and equal than"]
        }
    }
  }
</script>
<style>
    .el-select .el-input {
    width: 130px;
  }
  .input-with-select .el-input-group__prepend {
    background-color: #fff;
  }
</style>
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
        <el-form-item label="select column" v-for="column in query.filterList">
            <label>{{ column.name }}</label>
            <el-input v-model="column.value" class="input-with-select" size="mini">
                <el-select v-if="column.type === 'int' || 'float'" v-model="column.operator" placeholder="select" size="mini" slot="prepend">
                    <el-option
                      v-for="(operator, index) in numberOperators"
                      :key="index"
                      :label="operator"
                      :value="operator">
                    </el-option>
                </el-select>
                <el-select v-else v-model="column.operator" placeholder="select" size="mini" slot="prepend">
                    <el-option
                      v-for="(operator, index) in stringOperators"
                      :key="index"
                      :label="operator"
                      :value="operator">
                    </el-option>
                </el-select>
            </el-input>
        </el-form-item>
        <el-form-item>

        </el-form-item>
  </el-form>
</template>

<script>
  module.exports = {
    props: ['column_list'],
    methods: {
        addRule () {
            for (column_item of this.column_list) {
                if (this.addColumn == column_item.name) {
                    this.query.filterList.push(column_item);
                }
            }
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
            matchType: ["all", "any"],
            addColumn: "",
            stringOperators: ["equals", "contains", "begin with", "end with", "is empty", "is not empty"],
            numberOperators: ["equals", "greater than", "less than"]
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
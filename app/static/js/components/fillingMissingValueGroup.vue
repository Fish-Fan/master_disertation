<template>
    <div style="margin-top: 20px">
      <el-tabs v-model="activeTab" type="card">
        <el-tab-pane
                v-for="item in column_list"
                :label="item.column"
                :name="item.column"
                :key="item.index"
        >
            <el-form ref="form" :model="item.data">
                <el-form-item label="choose your filling way">
                    <el-select v-model="item.data.fillWay" placeholder="select">
                        <el-option
                          v-for="(option, index) in fillWayOptions"
                          :key="index"
                          :label="option"
                          :value="option">
                        </el-option>
                    </el-select>
                </el-form-item>
                <el-form-item v-if="item.data.fillWay == 'manual'" label="fill the missing value">
                    <el-input v-model="item.data.fillValue"></el-input>
                </el-form-item>
                <div v-else>
                    <el-form-item label="fill the missing value">
                    <el-select v-model="item.data.fillMethod" placeholder="select">
                        <el-option
                          v-for="(option, index) in fillWayMethods"
                          :key="index"
                          :label="option"
                          :value="option">
                        </el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="fill value">
                    <el-input v-model="item.data.fillValue" :disabled="true"></el-input>
                </el-form-item>
                </div>
                <el-form-item>
                    <el-button type="success" @click="addRecipe(item.data)" size="mini" plain >Add Recipe</el-button>
                </el-form-item>
            </el-form>
        </el-tab-pane>
      </el-tabs>
    </div>
</template>
<script>
  module.exports = {
    props: ['column_list'],
    devServer: {
        proxy: 'http://127.0.0.1:5000/'
    },
    methods: {
      addRecipe(fillItem) {
          fillItem.column = this.activeTab;
          fillMissingValueRecipe = {
              type: 'fillMissingValue',
              description: this.concatRecipeDescription(fillItem),
              data: fillItem
          }
        this.$emit('fill-missing-value-recipe-event', fillMissingValueRecipe)
      },
      concatRecipeDescription(fillItem) {
          return 'fill missing value in ' + fillItem.column + ' column with value "' + fillItem.fillValue + '" via ' + fillItem.fillMethod + ' method.'
      },
      calculateActiveTab() {
          if (this.column_list.length != 0) {
              return this.column_list[0].column
          } else {
              return ''
          }
      }
    },
    data() {
      return {
        activeTab: this.calculateActiveTab(),
        fillWay: '',
        fillWayOptions: ['manual', 'calculating'],
        fillWayMethods: ['frequency', 'average', 'mean'],
        fillMethod: '',
        form: {}
      }
    },
    watch: {
        column_list: function(newVal, oldVal) {
            this.activeTab = newVal[0].column
        }
    }
  }
</script>
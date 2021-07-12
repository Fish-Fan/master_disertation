<template>
  <el-tabs value="View">
    <el-tab-pane label="Data Preview" name="View">
      <el-table
        :key="tableKey"
        :data="tableData"
        :cell-class-name="cellClassNameFunc"
        style="width: 100%"
        height="450"
        border
        v-loading="isLoad"
        size="mini">
          <el-table-column
              v-for="item in headers"
              :prop="item.prop"
              :label="item.label"
              :index="item.index"
              width="180">
          </el-table-column>

      </el-table>
    </el-tab-pane>
  </el-tabs>


</template>

<style>
  .el-table .warning-row {
    background: oldlace;
  }

  .el-table .success-row {
    background: #f0f9eb;
  }
</style>


<script>
    module.exports = {
        props: ['highlight_columns', 'preview_dataset'],
        devServer: {
            proxy: 'http://127.0.0.1:5000/'
        },
        async mounted() {
            this.$http.get('/demodataset').then(response => {
               this.tableData = response.body.tableData;
               this.headers = response.body.headers;
            })
        },
        methods: {
          cellClassNameFunc({row, column, rowIndex, columnIndex}) {
            if (columnIndex == this.highlight_columns) {
              return 'warning-row'
            }
          }
        },
        watch: {
          highlight_columns: function(newVal, oldVal) {
            this.tableKey++
          },
          preview_dataset: function(newVal, oldVal) {
            this.tableData = newVal['tableData']
            this.headers = newVal['headers']
          }
        },
        data() {
            return {
                tableKey: 1,
                isLoad: false,
                tableData: [],
                headers: []
            }
        }
    }
</script>
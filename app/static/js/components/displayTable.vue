<template>
  <el-tabs value="View">
    <el-tab-pane label="Data Preview" name="View">
        <u-table
          v-loading="loading"
          ref="plTable"
          :cell-class-name="cellClassNameFunc"
          :data="tableData"
          height="450"
          use-virtual
          size="mini"
          :fit="true"
          :show-header="true"
          border>
          <u-table-column
             v-for="item in headers"
             :prop="item.prop"
             :label="item.label"
             :index="item.index"/>
        </u-table>
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
            this.loading = true;
            this.tableData = newVal['tableData'];
            this.headers = newVal['headers'];
            setTimeout(() => {
                this.loading = false;
            }, 2000);
          }
        },
        data() {
            return {
                tableKey: 1,
                isLoad: false,
                tableData: [],
                headers: [],
                loading: false
            }
        }
    }
</script>
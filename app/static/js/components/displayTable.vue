<template>
  <el-tabs value="View">
    <el-tab-pane label="Data Preview" name="View" style="height: 300px; margin-bottom: 20px">
        <u-table
          v-if="isGroupby"
          v-loading="loading"
          ref="multiheaders_table"
          :cell-class-name="cellClassNameFunc"
          :data="tableData"
          use-virtual
          size="mini"
          max-height="300"
          :fit="true"
          :show-header="true"
          border>
          <u-table-column label="index" :key="Math.random()">
                <u-table-column
                     v-for="item in indexes"
                     :prop="item.prop"
                     :label="item.label"
                     :key="Math.random()"
                     :index="item.index">
                </u-table-column>
          </u-table-column>
          <u-table-column label="columns" :key="Math.random()">
                <u-table-column
                     v-for="item in columns"
                     :prop="item.prop"
                     :label="item.label"
                     :key="Math.random()"
                     :index="item.index">
                </u-table-column>
          </u-table-column>
        </u-table>

        <u-table
          v-else
          v-loading="loading"
          ref="simple_table"
          :cell-class-name="cellClassNameFunc"
          :data="tableData"
          use-virtual
          size="mini"
          max-height="300"
          :fit="true"
          :show-header="true"
          border>
            <u-table-column
             v-for="item in headers"
             :prop="item.prop"
             :label="item.label"
             :key="Math.random()"
             :render-header="linefeed"
             :index="item.index">
            </u-table-column>
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
        props: ['highlight_columns', 'preview_dataset', 'is_loading'],
        devServer: {
            proxy: 'http://127.0.0.1:5000/'
        },
        methods: {
          linefeed (h,{column,index}) {
                let number = column.label.length;
                let size = 10;
                column.minWidth = number*size;
                return h('div',{class:'table-head',style:{width:'80%'}},[column.label])
            },
          cellClassNameFunc({row, column, rowIndex, columnIndex}) {
            if (this.isGroupby) {
                if (columnIndex - this.indexes.length == this.highlight_columns) {
                    return 'warning-row'
                }
            } else {
                if (columnIndex == this.highlight_columns) {
                    return 'warning-row'
                }
            }
          }
        },
        watch: {
          highlight_columns: function(newVal, oldVal) {
            this.tableKey++
          },
          preview_dataset: function(newVal, oldVal) {
            this.tableData = newVal['tableData'];
            this.headers = newVal['headers'];
            this.isGroupby = newVal['isGroupby'];
            this.indexes = newVal['indexes'];
            this.columns = newVal['columns'];
          },
           is_loading: function(newVal, oldVal) {
                this.loading = newVal
            }
        },
        data() {
            return {
                tableKey: 1,
                tableData: [],
                /*for normal table*/
                headers: [],
                /*for group by table*/
                indexes: [],
                columns: [],
                isGroupby: false,
                loading: false
            }
        }
    }
</script>
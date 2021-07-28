<template>
    <el-tabs value="Data Profiling">
        <el-tab-pane v-loading="loading" label="Data Profiling" name="Data Profiling">
            <el-radio-group
              v-model="highlightColumn"
              size="small"
              @change="highlightColumnMethod"
              >
            <el-radio-button  v-for="column in column_list"
                                 :label="column.index"
                                 :value="column.index"
                                 :key="column.index">
                {{ column.name }}
            </el-radio-button>
        </el-radio-group>
        </el-tab-pane>
    </el-tabs>
</template>
<script>
  module.exports = {
    props: ['column_list', 'is_loading'],
    devServer: {
        proxy: 'http://127.0.0.1:5000/'
    },
    methods: {
      async highlightColumnMethod(index) {
          var column_item = this.column_list[index];
          this.$http.post('/column_profiling', {
              column: column_item.name
          }).then(response => {
              this.$emit('column-profiling-result', response.body);
              this.$emit('highlight-columns-changed', {index: column_item.index})
          });

      }
    },
    watch: {
        column_list: function (newVal, oldVal) {
            this.column_list = newVal;
        },
        is_loading: function(newVal, oldVal) {
            this.loading = newVal
        }

    },
    data() {
      return {
        highlightColumn: 'string',
        loading: false
      }
    }
  }
</script>
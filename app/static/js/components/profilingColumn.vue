<template>
    <div style="margin-top: 20px">
      <el-radio-group
              v-model="highlightColumn"
              size="small"
              @change="highlightColumnMethod"
              >
        <el-radio-button  v-for="column in column_list"
                             :label="column.name"
                             :value="column.index"
                             :key="column.index">
            {{ column.name }}
        </el-radio-button>
      </el-radio-group>

    </div>
</template>
<script>
  module.exports = {
    props: ['column_list'],
    devServer: {
        proxy: 'http://127.0.0.1:5000/'
    },
    methods: {
      async highlightColumnMethod() {
          column_name = this.highlightColumn;
          column_index = this.column_list[column_name];
          this.$http.post('/column_profiling', {
              column: column_name
          }).then(response => {
              this.$emit('column-profiling-result', response.body);
              this.$emit('highlight-columns-changed', {index: column_index})
          });

      }
    },
    watch: {
        column_list: function (newVal, oldVal) {
            this.column_list = newVal;
        }
    },
    data() {
      return {
        highlightColumn: 'string'
      }
    }
  }
</script>
<template>
    <div style="margin-top: 20px">
      <el-radio-group
              v-model="highlightColumn"
              size="small"
              @change="highlightColumnMethod"
              >
        <el-radio-button  v-for="(index, name) in column_list"
                             :label="name"
                             :value="index"
                             :key="index">
            {{ name }}
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
          // const requestOptions = {
          //       method: "POST",
          //       headers: { 'Accept': 'application/json', "Content-Type": "application/json"},
          //       body: JSON.stringify({ column: column_name })
          //      };
          // const res = await fetch('/column_profiling', requestOptions);
          // result = await res.json();
          this.$http.post('/column_profiling', {
              column: column_name
          }).then(response => {
              this.$emit('column-profiling-result', response.body);
              this.$emit('highlight-columns-changed', {index: column_index})
          });

      }
    },
    data() {
      return {
        highlightColumn: 'string'
      }
    }
  }
</script>
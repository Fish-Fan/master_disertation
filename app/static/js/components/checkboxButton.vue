<template>
    <div style="margin-top: 20px">
      <el-checkbox-group v-model="submitDeleteColumns" size="small" @change="highlightColumn()">
        <el-checkbox-button  v-for="item in column_list" :label="item.column" :value="item.column" :key="item.index">{{item.column}}</el-checkbox-button>
      </el-checkbox-group>
    </div>
</template>
<script>
  module.exports = {
    props: ['column_list'],
    methods: {
      highlightColumn() {
          console.log(this.submitDeleteColumns)
      }
    },
    data() {
      return {
        submitDeleteColumns: []
      }
    }
  }
</script>
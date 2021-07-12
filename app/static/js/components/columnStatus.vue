<template>
    <el-tabs value="View">
        <el-tab-pane label="Column Profiling Result" name="View">
            <el-tag
                v-for="(item, key) in column_profiling_result"
                effect="dark"
                :type="item.type"
                style="margin: 10px 10px 5px 0"
            >
                {{ key }} : {{ item.value }}
            </el-tag>
        </el-tab-pane>
    </el-tabs>
</template>

<script>
  module.exports = {
    props: ['column_profiling_result'],
    methods: {

    },
    data() {
      return {
        submitDeleteColumns: []
      }
    }
  }
</script>
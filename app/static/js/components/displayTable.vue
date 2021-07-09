<template>
  <el-table
    :data="tableData"
    style="width: 100%"
    height="450"
    border
    size="mini">
    <el-table-column
      prop="name"
      label="name"
      width="180">
    </el-table-column>
    <el-table-column
      prop="company_name"
      label="company_name"
      width="180">
    </el-table-column>
    <el-table-column
      prop="address"
      label="address">
    </el-table-column>
      <el-table-column
      prop="county"
      label="county">
    </el-table-column>
      <el-table-column
      prop="postal"
      label="postal">
    </el-table-column>
      <el-table-column
      prop="email"
      label="email">
    </el-table-column>
      <el-table-column
      prop="web"
      label="web">
    </el-table-column>
      <el-table-column
      prop="phone"
      label="phone">
    </el-table-column>
      <el-table-column
      prop="age"
      label="age">
    </el-table-column>

  </el-table>
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
        devServer: {
            proxy: 'http://127.0.0.1:5000/'
        },
        async mounted() {
            const requestOptions = {
                method: "POST",
                headers: { 'Accept': 'application/json', "Content-Type": "application/json"},
                body: JSON.stringify({ filename: this.filename })
            };
            const res = await fetch('/demodataset', requestOptions);
            result = await res.json();
            this.tableData = result.tableData;
        },
        methods: {

        },
        data() {
            return {
                tableData: []
            }
        }
    }
</script>
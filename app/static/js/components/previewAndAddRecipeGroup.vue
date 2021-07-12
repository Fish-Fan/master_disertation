<template>
    <div style="margin-top: 20px">
        <el-form>
            <el-form-item>
                <el-button type="primary" @click="preview">Preview</el-button>
                <el-button>Add Recipe</el-button>
            </el-form-item>
        </el-form>
    </div>
</template>
<script>
  module.exports = {
    props: ['preview_delete_columns', 'preview_fill_missing_columns', 'preview_splitting_columns', 'preview_change_type_columns'],
    devServer: {
        proxy: 'http://127.0.0.1:5000/'
    },
    methods: {
        async preview() {
            fillMissingValueData = this.preProcessFillMissingValueData();
            // console.log(fillMissingValueData);
            // const requestOptions = {
            //     method: "POST",
            //     headers: { 'Accept': 'application/json', "Content-Type": "application/json"},
            //     body: JSON.stringify({
            //         deleteObj: {columns: this.preview_delete_columns},
            //         fillingMissingObj: {columns: fillMissingValueData}
            //     })
            //    };
            //   const res = await fetch('/preview', requestOptions);

            this.$http.post('/preview', {
                    deleteObj: {columns: this.preview_delete_columns},
                    fillingMissingObj: {columns: fillMissingValueData}
                }).then(response => {
                    this.$emit('preview-dataset-changed', response.body)
            })

        },
        preProcessFillMissingValueData() {
            ansMap = new Map();
            for (const item of this.preview_fill_missing_columns) {
                ansMap.set(item.column, item.fillValue)
            }
            ans = [];
            for(let [key, value] of ansMap) {
                ans.push({
                    column: key,
                    fillValue: value
                })
            }
            return ans
        }

    },
    data() {
      return {

      }
    },
    watch: {

    }
  }
</script>
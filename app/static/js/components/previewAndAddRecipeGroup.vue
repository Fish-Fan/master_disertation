<template>
    <el-form>
            <el-form-item>
                <el-button type="primary" @click="preview">Preview</el-button>
                <el-button>Add Recipe</el-button>
            </el-form-item>
    </el-form>
</template>
<script>
  module.exports = {
    props: ['recipe_list'],
    devServer: {
        proxy: 'http://127.0.0.1:5000/'
    },
    methods: {
        async preview() {
            fillMissingValueData = this.preProcessFillMissingValueData();
            this.$http.post('/preview', {
                    deleteObj: {columns: this.preview_delete_columns},
                    fillingMissingObj: {columns: fillMissingValueData},
                    splittingObj: {columns: this.preview_splitting_columns},
                    changeTypeObj: {columns: this.preview_change_type_columns}
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
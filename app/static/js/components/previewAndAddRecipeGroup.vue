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
            this.$http.post('/preview', {
                    recipe_list: this.recipe_list
                }).then(response => {
                    this.$emit('preview-dataset-changed', response.body)
            })

        },
    },
    data() {
      return {

      }
    },
    watch: {

    }
  }
</script>
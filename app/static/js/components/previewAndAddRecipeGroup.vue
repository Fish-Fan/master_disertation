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
            this.$emit('is-loading-event', true);
            this.$http.post('/preview', {
                    recipe_list: this.recipe_list
                }).then(response => {
                    if (response.body.code == 500) {
                        this.$message.error(response.body.message);
                    } else {
                        this.$emit('preview-dataset-changed', response.body);
                    }
                    this.$emit('is-loading-event', false);
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
<template>
    <div style="float: left">
        <el-button size="mini" v-if="has_profiled_prop" type="primary" @click="preview">Preview</el-button>
        <el-button size="mini" v-else type="primary" @click="profiling">profiling</el-button>
        <el-button size="mini" type="button" type="info" data-dismiss="modal">Close</el-button>
    </div>
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
        profiling(e) {
            e.preventDefault();
            this.$emit('is-loading-event', true);
            this.has_profiled_prop = true;
            this.$http.post('/profiling', {}).then(response => {
                this.$emit('is-loading-event', false);
                this.$emit('profiling-event', response.body)
            });

            this.$http.get('/getdataset').then(response => {
               this.$emit('get-data-set-event', response.body)
            })
        },
    },
    data() {
      return {
        has_profiled_prop: false
      }
    },
    watch: {

    }
  }
</script>
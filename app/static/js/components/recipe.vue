<template>
    <el-tabs value="View">
        <el-tab-pane label="Recipe" name="View">
            <el-timeline>
                <el-timeline-item v-for="recipe in recipe_list" :timestamp="recipe.type" placement="top">
                  <el-card>
                    <p>{{ recipe.description }}</p>
                  </el-card>
                </el-timeline-item>
            </el-timeline>
        </el-tab-pane>
    </el-tabs>
</template>
<script>
  module.exports = {
    props: ['recipe_list'],
    devServer: {
        proxy: 'http://127.0.0.1:5000/'
    },
    methods: {

    },
    data() {
      return {

      }
    },
    watch: {

    }
  }
</script>
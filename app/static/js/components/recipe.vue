<template>
    <el-tabs value="View">
        <el-tab-pane label="Recipe" name="View">
            <el-timeline>
                <el-timeline-item v-for="(recipe, index) in recipe_list" :timestamp="recipe.type" placement="top">
                  <el-card>
                    <el-button style="float: right; padding: 3px 0" type="text" icon="el-icon-remove" @click="removeRecipeItem(index)"></el-button>
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
        removeRecipeItem(index) {
            this.$emit('remove-recipe-item-event', {item_index: index});
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
<template>
    <div style="margin-top: 20px">
      <el-checkbox-group
              v-model="submitDeleteColumns"
              size="small"
              >
        <el-checkbox-button  v-for="item in column_list"
                             :label="item.column"
                             :value="item.column"
                             :key="item.index">{{item.column}}</el-checkbox-button>
      </el-checkbox-group>

        <el-button type="success" @click="addRecipe" size="mini" plain>Add Recipe</el-button>

    </div>
</template>
<script>
  module.exports = {
    props: ['column_list'],
    devServer: {
        proxy: 'http://127.0.0.1:5000/'
    },
    methods: {
      addRecipe() {
        deleteRecipe = {
            type: 'deleteColumn',
            description: this.concatRecipeDescription(),
            data: this.submitDeleteColumns
        };
        this.$emit('delete-recipe-event', deleteRecipe)
      },
      concatRecipeDescription() {
          return 'Remove ' + this.submitDeleteColumns.join() + ' from this dataset.'

      }


    },
    data() {
      return {
        submitDeleteColumns: []
      }
    }
  }
</script>
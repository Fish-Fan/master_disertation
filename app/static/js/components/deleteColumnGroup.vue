<template>
    <div style="margin-top: 20px">
        <p>suggestions:</p>
      <el-checkbox-group
              v-model="submitDeleteColumns_suggest"
              size="small"
              >
          <el-checkbox
                  v-for="item in delete_list"
                             :label="item.column"
                             :value="item.column"
                             :key="item.index"
          border>{{item.column}}
          </el-checkbox>

          <el-divider></el-divider>
      </el-checkbox-group>

        <p>other columns: </p>

      <el-checkbox-group
              v-model="submitDeleteColumns_normal"
              size="small"
              >
        <el-checkbox-button  v-for="item in normalColumns"
                             :label="item.name"
                             :value="item.name"
                             :key="item.index">{{item.name}}</el-checkbox-button>
      </el-checkbox-group>

        <el-button type="success" @click="addRecipe" size="mini" plain>Add Recipe</el-button>

    </div>
</template>
<script>
  module.exports = {
    props: ['column_list', 'delete_list'],
    devServer: {
        proxy: 'http://127.0.0.1:5000/'
    },
    methods: {
      addRecipe() {
        var submit_delete_column = this.computeSubmitDeleteColumns();
        deleteRecipe = {
            type: 'deleteColumn',
            description: this.concatRecipeDescription(submit_delete_column),
            data: submit_delete_column
        };
        this.$emit('delete-recipe-event', deleteRecipe)
      },
      concatRecipeDescription(submit_delete_column) {
          return 'Remove ' + submit_delete_column.join() + ' from this dataset.'

      },
      computeSubmitDeleteColumns() {
          return this.submitDeleteColumns_suggest.concat(this.submitDeleteColumns_normal);
      }

    },
    watch: {
        column_list: function(newVal, oldVal) {
            var otherColumnsArr = [];
            for (column of newVal) {
                var count = 0;
                for (delete_column of this.delete_list) {
                    if (delete_column.column == column.name) {
                        count += 1;
                    }
                }
                if (count == 0) {
                    otherColumnsArr.push(column);
                }
            }
            this.normalColumns = otherColumnsArr;
        },
        delete_list: function(newVal, oldVal) {
            this.submitDeleteColumns_suggest = [];
            this.submitDeleteColumns_normal = [];
        }
    },
    data() {
      return {
        submitDeleteColumns_suggest: [],
        submitDeleteColumns_normal: [],
        normalColumns: []
      }
    }
  }
</script>
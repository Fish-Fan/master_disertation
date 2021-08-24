<template>
    <div style="margin-top: 20px" v-loading="loading">
       <div v-for="suggest_obj in submitDeleteColumns_suggest_render">
            <p> {{ suggest_obj.type }} </p>
              <el-checkbox-group
                      v-model="submitDeleteColumns_suggest"
                      size="small"
                      >
                  <el-checkbox
                          v-for="item in suggest_obj.arr"
                                     :label="item.column"
                                     :value="item.column"
                                     :key="item.index"
                  border><i v-if="item.recommend" class="el-icon-star-on"></i> {{item.column}}
                  </el-checkbox>

                  <el-divider></el-divider>
              </el-checkbox-group>
       </div>

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
    props: ['column_list', 'delete_list', 'is_loading'],
    devServer: {
        proxy: 'http://127.0.0.1:5000/'
    },
    methods: {
      addRecipe() {
        var submit_delete_column = this.computeSubmitDeleteColumns();
        deleteRecipe = {
            type: 'DeleteColumn',
            description: this.concatRecipeDescription(submit_delete_column),
            data: submit_delete_column,
            guidance_category: 'clean'
        };
        this.$emit('delete-recipe-event', deleteRecipe)
      },
      concatRecipeDescription(submit_delete_column) {
          return 'Remove ' + submit_delete_column.join() + ' from this dataset.'

      },
      computeSubmitDeleteColumns() {
          return this.submitDeleteColumns_suggest.concat(this.submitDeleteColumns_normal);
      },
      computesubmitDeleteColumns_suggest(newVal) {
          var delete_column_suggest = [];
          var delete_column_map = new Map();
          delete_column_map.set('missing', []);
          delete_column_map.set('constant', []);
          delete_column_map.set('zero', []);
          for (item of newVal) {
              arr = delete_column_map.get(item.description);
              arr.push(item);
          }

          for (let [type, arr] of delete_column_map) {
              delete_column_suggest.push({'type': type, 'arr': arr});
          }
          this.submitDeleteColumns_suggest_render = delete_column_suggest;
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
            this.computesubmitDeleteColumns_suggest(newVal);
            this.submitDeleteColumns_suggest = [];
            this.submitDeleteColumns_normal = [];
        },
        is_loading: function(newVal, oldVal) {
            this.loading = newVal;
        }
    },
    data() {
      return {
        submitDeleteColumns_suggest: [],
        submitDeleteColumns_normal: [],
        submitDeleteColumns_suggest_render: [],
        normalColumns: [],
        loading: false
      }
    }
  }
</script>
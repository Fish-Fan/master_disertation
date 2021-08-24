<template>
    <el-tabs value="View">
        <el-tab-pane label="Recipe" name="View">
            <div v-if="this.recipe_guidance_skeleton.length > 0">
                <el-card class="box-card" v-for="card in this.recipe_guidance_skeleton">
                  <div slot="header" class="clearfix">
                    <span>{{card.type}}</span>
                  </div>
                  <div v-if="card.steps.length == 0">
                    {{card.description}}
                  </div>
                  <div v-else>
                      <el-timeline>
                            <el-timeline-item v-for="(recipe, index) in card.steps" :timestamp="recipe.type" placement="top">
                              <el-card>
                                <el-button style="float: right; padding: 3px 0" type="text" icon="el-icon-remove" @click="removeRecipeGuidanceItem(index, card.type)"></el-button>
                                <p>{{ recipe.description }}</p>
                              </el-card>
                            </el-timeline-item>
                        </el-timeline>
                  </div>
                </el-card>
            </div>
            <div v-else>
                <el-timeline>
                    <el-timeline-item v-for="(recipe, index) in recipe_list" :timestamp="recipe.type" placement="top">
                      <el-card>
                        <el-button style="float: right; padding: 3px 0" type="text" icon="el-icon-remove" @click="removeRecipeItem(index)"></el-button>
                        <p>{{ recipe.description }}</p>
                      </el-card>
                    </el-timeline-item>
                </el-timeline>
            </div>
        </el-tab-pane>
    </el-tabs>
</template>
<script>
  module.exports = {
    props: ['recipe_list', 'recipe_guidance_skeleton'],
    devServer: {
        proxy: 'http://127.0.0.1:5000/'
    },
    methods: {
        removeRecipeItem(index) {
            this.$emit('remove-recipe-item-event', {item_index: index});
        },
        removeRecipeGuidanceItem(index, category) {
            this.$emit('remove-recipe-guidance-item-event', {
                item_index: index,
                guidance_category: category
            });
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
<template>
    <el-tabs v-model="activeTab" tab-position="top">
        <el-tab-pane
                v-for="column_item in column_list"
                :name="column_item.column"
                :label="column_item.column"
                :key="column_item.index"
        >
            <el-form ref="form" :model="column_item">
                <el-form-item label="choose your column type">
                    <el-select v-model="column_item.data.type" placeholder="select" @change="handleDelimiterChangeEvent(column_item_obj.form)">
                        <el-option
                          v-for="(typeOption, index) in typeOptions"
                          :key="index"
                          :label="typeOption"
                          :value="typeOption">
                        </el-option>
                    </el-select>
                </el-form-item>

                <el-form-item>
                    <el-button type="success" @click="addRecipe(column_item)" size="mini" plain >Add Recipe</el-button>
                </el-form-item>
            </el-form>
        </el-tab-pane>
    </el-tabs>
</template>

<script>
  module.exports = {
    props: ['column_list'],
    methods: {
        computedActiveTab: function () {
            if (this.column_list.length != 0) {
                return column_list[0].column;
            } else {
                return ''
            }
        },
        concatenateDescription: function(changeItem) {
            return 'change ' + changeItem.column + ' column type into ' + changeItem.data.type;
        },
        addRecipe(changeItem) {
            changeItem.column = this.activeTab;
            changeColumnTypeRecipe = {
                type: 'changeColumnType',
                description: this.concatenateDescription(changeItem),
                data: changeItem
            };
            this.$emit('change-column-type-event', changeColumnTypeRecipe);
        }
    },
    computed: {

    },
    watch: {
        column_list: function(newVal, oldVal) {
            this.activeTab = newVal[0].column
        }
    },
    data() {
      return {
          submitSplitColumns: [],
          activeTab: this.computedActiveTab(),
          typeOptions: [
              'string',
              'int',
              'float',
              'email',
              'postal'
          ]
      }
    }
  }
</script>
<template>
    <el-tabs v-model="activeTab" tab-position="top" v-loading="loading">
        <el-tab-pane
                v-for="column_item in column_list"
                :name="column_item.column"
                :key="Math.random() + '-' + column_item.index"
        >
            <span slot="label"><i v-if="column_item.recommend" class="el-icon-star-on"></i> {{column_item.column}}</span>
            <el-form ref="form" :model="column_item">
                <el-form-item label="choose your column type">
                    <el-select v-model="column_item.data.type" placeholder="select" size="mini">
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
    props: ['column_list', 'is_loading'],
    methods: {
        concatenateDescription: function(changeItem) {
            return 'change ' + changeItem.column + ' column type into ' + changeItem.data.type;
        },
        addRecipe(changeItem) {
            var data_obj = {
                column : this.activeTab,
                index: changeItem.index,
                data: {
                    type: changeItem.data.type
                }
            };

            var changeColumnTypeRecipe = {
                type: 'ChangeColumnType',
                description: this.concatenateDescription(data_obj),
                data: data_obj,
                guidance_category: 'enrich'
            };
            this.$emit('change-column-type-event', changeColumnTypeRecipe);
        }
    },
    computed: {

    },
    watch: {
        column_list: function (newVal, oldVal) {
            if (newVal.length > 0) {
                this.activeTab = newVal[0].column;
            }
        },
        is_loading: function(newVal, oldVal) {
            this.loading = newVal;
        }
    },
    data() {
        return {
            activeTab: '',
            typeOptions: [
                'string',
                'int',
                'float',
                'email',
                'postal',
                'category'
            ],
            loading: false
        }
    }
  }


</script>
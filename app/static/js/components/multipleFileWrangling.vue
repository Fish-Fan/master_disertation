<template>
  <el-tabs value="View">
      <el-button type="primary" @click="handlePickDatasetClick">Choose another dataset</el-button>

      <el-dialog
          title="Choose another dataset"
          :visible.sync="dialogVisible"
          width="30%"
          >

          <div v-for="dataset in dataset_list">
                  <el-radio v-model="dataset_submit" :label="dataset" border> {{dataset}} </el-radio>
          </div>

          <span slot="footer" class="dialog-footer">
            <el-button @click="dialogVisible = false">Cancel</el-button>
            <el-button type="primary" @click="handleConfirmClick">Confirm</el-button>
          </span>
        </el-dialog>

    <el-tab-pane label="Data Concatenation" name="Concatenation" style="height: 450px; margin-bottom: 20px">
        <u-table
          v-loading="loading"
          ref="simple_table"
          :data="tableData"
          use-virtual
          size="mini"
          max-height="450"
          :fit="true"
          :show-header="true"
          border>
            <u-table-column
                prop="column_name"
                label="column_name"
                :key="Math.random()"
                width="180">
            </u-table-column>
            <u-table-column
                prop="matched_column"
                label="matched_column">
                :key="Math.random()"
                <template v-slot="scope">
                    <el-select v-model="scope.row.matched_column" size="mini">
                         <el-option v-for="item in concatenate_columns" :key="item.index" :label="item.name" :value="item.name"></el-option>
                   </el-select>
                </template>
            </u-table-column>
            <u-table-column
                prop="score"
                label="score"
                :key="Math.random()"
                width="180">
            </u-table-column>

        </u-table>
        <el-button type="success" @click="addConcatenationRecipe" size="mini" plain >Add Recipe</el-button>
    </el-tab-pane>
    <el-tab-pane label="Data Join" name="Join" style="height: 450px; margin-bottom: 20px">
        <el-form ref="JoinForm">
            <el-form-item label="choose your left join key">
                    <el-select v-model="left_join_key_1" placeholder="select" size="mini">
                        <el-option
                          v-for="(option, index) in column_list"
                          :key="index"
                          :label="option.name"
                          :value="option.name">
                        </el-option>
                    </el-select>
                    <el-select v-model="left_join_key_2" placeholder="select" size="mini">
                        <el-option
                          v-for="(option, index) in concatenate_columns"
                          :key="index"
                          :label="option.name"
                          :value="option.name">
                        </el-option>
                    </el-select>
                </el-form-item>
        </el-form>
        <el-button type="success" @click="addJoinRecipe" size="mini" plain >Add Recipe</el-button>
    </el-tab-pane>
  </el-tabs>


</template>

<script>
    module.exports = {
        props: ['is_loading', 'column_list'],
        devServer: {
            proxy: 'http://127.0.0.1:5000/'
        },
        methods: {
          computeLeftJoinSubmit() {
              return {
                  'left_on': this.left_join_key_1,
                  'right_on': this.left_join_key_2
              }
          },
          joinRecipeDescription() {
              return 'left join new dataset, join condition: ' + this.left_join_key_1 + ' = ' + this.left_join_key_2
          },
          addJoinRecipe() {
              joinRecipe = {
                  type: 'join',
                  description: this.joinRecipeDescription(),
                  data: this.computeLeftJoinSubmit()
              };
              this.$emit('join-recipe-event', joinRecipe)
          },
          concatRecipeDescription(new_column_name_list_submit) {
                return 'change new dataset column names into ' + new_column_name_list_submit.toString() + ' for concatenation.'
          },
          addConcatenationRecipe() {
              this.computeNewColumnNamesSubmit();
              concatenationRecipe = {
                  type: 'concat',
                  description: this.concatRecipeDescription(this.new_column_name_list_submit),
                  data: this.new_column_name_list_submit
              };
              this.$emit('concat-recipe-event', concatenationRecipe)
          },
          computeNewColumnNamesSubmit() {
              var new_column_name_arr = [];
              for (table_data_obj of this.tableData) {
                    if (table_data_obj.matched_column) {
                        new_column_name_arr.push({'origin_name': table_data_obj.matched_column, 'new_name': table_data_obj.column_name});
                    }
              }
              this.new_column_name_list_submit = new_column_name_arr;
          },
          computeTableData(column_list) {
              var tableData = [];
              for (column_obj of column_list) {
                    var table_data_item = {};
                    table_data_item.column_name = column_obj.name;
                    table_data_item.index = column_obj.index;
                    table_data_item.type = column_obj.type;

                    var matched_obj = this.concatenate_result[table_data_item.column_name];
                    if (matched_obj) {
                        table_data_item.matched_column = matched_obj.matched_column;
                        table_data_item.score = matched_obj.score;
                    }
                    tableData.push(table_data_item);
              }
              this.tableData = tableData;
          },
          handlePickDatasetClick() {
              this.$http.get('/dataset').then(response => {
                  result = response.body;
                  this.dataset_list = result;
                  this.dialogVisible = true;
              });
          },
          handleConfirmClick() {
            this.$http.post('/multiple_file_wrangling', {
                dataset_submit: this.dataset_submit
            }).then(response => {
                  result = response.body;
                  this.concatenate_result = result.concatenate_result;
                  this.join_result = result.join_result;
                  this.dialogVisible = false;

                  /*concatenation part*/
                  this.computeTableData(this.column_list);
                  this.concatenate_columns = result.concatenate_columns;
                  /*join part*/
                  this.left_join_key_1 = this.join_result.join_keys[0];
                  this.left_join_key_2 = this.join_result.join_keys[1];
              });
          }
        },
        watch: {
           is_loading: function(newVal, oldVal) {
                this.loading = newVal
            }
        },
        data() {
            return {
                activeTab: "Concatenation",
                dialogVisible: false,
                dataset_list: [],
                dataset_submit: "",
                concatenate_result: [],
                join_result: {},
                tableData: [],
                concatenate_columns: [],
                left_join_key_1: "",
                left_join_key_2: "",
                new_column_name_list_submit: [],
                loading: false
            }
        }
    }
</script>
<template>
    <div v-loading="loading">
        <el-button style="margin-top: 20px" size="mini" type="primary" @click="dialogVisible = true">Choose another dataset</el-button>

          <el-dialog
              :append-to-body="true"
              title="Choose another dataset"
              :visible="dialogVisible"
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
      <el-tabs value="View" v-model="activeTab">
        <el-tab-pane label="Concatenation" name="Concatenation" style="margin-bottom: 20px">
            <span slot="label"><i v-if="concatenation_recommend" class="el-icon-star-on"></i> Concatenation </span>
            <u-table
              ref="simple_table"
              :data="tableData"
              use-virtual
              size="mini"
              :fit="true"
              :show-header="true"
              style="width: 80%"
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
        <el-tab-pane label="Join" name="Join" style="height: 450px; margin-bottom: 20px">
            <span slot="label"><i v-if="join_recommend" class="el-icon-star-on"></i> Join </span>
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
    </div>


</template>

<script>
    module.exports = {
        props: ['is_loading', 'column_list', 'refresh'],
        devServer: {
            proxy: 'http://127.0.0.1:5000/'
        },
        mounted() {
           this.$http.get('/dataset').then(response => {
                  result = response.body;
                  this.dataset_list = result;
              });
        },
        methods: {
          computeLeftJoinSubmit() {
              return {
                  'left_on': this.left_join_key_1,
                  'right_on': this.left_join_key_2
              }
          },
          joinRecipeDescription(dataset_submit) {
              return 'left join new dataset "' + dataset_submit +'", join condition: ' + this.left_join_key_1 + ' = ' + this.left_join_key_2
          },
          addJoinRecipe() {
              joinRecipe = {
                  type: 'join',
                  description: this.joinRecipeDescription(this.dataset_submit),
                  data: this.computeLeftJoinSubmit()
              };
              this.$emit('join-recipe-event', joinRecipe)
          },
          concatRecipeDescription(dataset_submit, new_column_name_list_submit) {
                return 'change new dataset "'+ dataset_submit +'" column names into ' + new_column_name_list_submit.toString() + ' for concatenation.'
          },
          addConcatenationRecipe() {
              this.computeNewColumnNamesSubmit();
              concatenationRecipe = {
                  type: 'concat',
                  description: this.concatRecipeDescription(this.dataset_submit, this.new_column_name_list_submit),
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
                        if (table_data_item.score >= 100) {
                            this.concatenation_recommend = true;
                        }
                    }
                    tableData.push(table_data_item);
              }
              this.tableData = tableData;
          },
          handleConfirmClick() {
            this.loading = true;
            this.dialogVisible = false;
            this.$http.post('/multiple_file_wrangling', {
                dataset_submit: this.dataset_submit
            }).then(response => {
                  result = response.body;
                  this.concatenate_result = result.concatenate_result;
                  this.join_result = result.join_result;
                  /*concatenation part*/
                  this.computeTableData(this.column_list);
                  this.concatenate_columns = result.concatenate_columns;
                  /*join part*/
                  this.left_join_key_1 = this.join_result.join_keys[0];
                  this.left_join_key_2 = this.join_result.join_keys[1];
                  if (this.join_result.score >= 100) {
                        this.join_recommend = true;
                  }
                  this.loading = false;
              });
          }
        },
        watch: {
           is_loading: function(newVal, oldVal) {
                this.loading = newVal
            },
           refresh: function (newVal, oldVal) {
               if (newVal) {
                    this.activeTab = "Concatenation";
                    this.dialogVisible = false;
                    this.dataset_submit = "";
                    this.concatenate_result = [];
                    this.join_result = {};
                    this.tableData = [];
                    this.concatenate_columns = [];
                    this.left_join_key_1 = "";
                    this.left_join_key_2 = "";
                    this.new_column_name_list_submit = [];
                    this.concatenation_recommend = false;
                    this.join_recommend = false;
                    this.loading = false;
               }
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
                concatenation_recommend: false,
                join_recommend: false,
                loading: false
            }
        }
    }
</script>
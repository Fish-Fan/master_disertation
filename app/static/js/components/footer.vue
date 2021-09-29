<template>
    <div>
        <el-button size="mini" v-if="has_profiled_prop" type="primary" @click="preview"  style="float: left">Preview</el-button>
        <el-button size="mini" v-else type="primary" @click="profiling"  style="float: left">Load Dataset</el-button>

        <vue-blob-json-csv
          file-type="csv"
          file-name="export_file"
          :data="preview_dataset.tableData"
        >
            <el-button size="mini"  style="float: left">Export</el-button>
        </vue-blob-json-csv>
        <el-button size="mini"  @click="RecipeManagement"  style="float: left">Manage Recipe</el-button>
        <el-button size="mini"  @click="uploadFile"  style="float: left">Upload</el-button>
        <el-button size="mini" type="success" data-dismiss="modal" style="float: right" @click="SaveRecipe">Save</el-button>
        <el-button size="mini"data-dismiss="modal" style="float: right">Close</el-button>



        <el-dialog
              :append-to-body="true"
              title="Purpose of this data wrangling task"
              :visible="domainKnowledgeDialogVisible"
              >

              <el-form ref="form" :model="domainKnowledge">
                    <p class="question_label">Need some guidance for generating a nice recipe in this data wrangling task?</p>
                    <el-radio-group v-model="domainKnowledge.needGuidance" >
                        <el-radio label="Yes" border>Yes</el-radio>
                        <el-radio label="No" border>No, just continue my exploration process</el-radio>
                      </el-radio-group>
                    <div v-if="domainKnowledge.needGuidance == 'Yes'">
                        <p class="question_label">Does this wrangling involve with single or multiple files?</p>
                        <el-radio-group v-model="domainKnowledge.singleOrMultiple" >
                            <el-radio label="Single" border>Single</el-radio>
                            <el-radio label="Multiple" border>Multiple</el-radio>
                          </el-radio-group>
                        <p class="question_label">Is this dataset tidy enough without any clean operation? For example, discard some irrelevant columns and deal with missing values</p>
                            <el-radio-group v-model="domainKnowledge.needClean" >
                                <el-radio label="Yes" border>Yes</el-radio>
                                <el-radio label="No" border>No</el-radio>
                              </el-radio-group>
                        <p class="question_label">Does every column meet its own semantic role requirement? For example, some headers are too vague that need to specify</p>
                            <el-radio-group v-model="domainKnowledge.needSplit">
                                <el-radio label="Yes" border>Yes</el-radio>
                                <el-radio label="No" border>No</el-radio>
                              </el-radio-group>
                        <p class="question_label">Making a conclusion? Any aggregate functions want to apply?</p>
                            <el-radio-group v-model="domainKnowledge.needAggregation">
                                <el-radio label="Yes" border>Yes</el-radio>
                                <el-radio label="No" border>No</el-radio>
                              </el-radio-group>
                    </div>
              </el-form>

              <span slot="footer" class="dialog-footer">
                <el-button @click="domainKnowledgeDialogVisible = false">Cancel</el-button>
                <el-button type="primary" @click="handleConfirmClick">Confirm</el-button>
              </span>
        </el-dialog>

        <el-dialog
              title="Upload File"
              :visible.sync="uploadDialogVisible"
                style="text-align: left"
              >
            <el-upload
                  class="upload-demo"
                  drag
                  action="http://127.0.0.1:5000/upload_file"
                  multiple>
                  <i class="el-icon-upload"></i>
                  <div class="el-upload__text">Drag and drop your file here, or<em>click here to upload</em></div>
                  <div class="el-upload__tip" slot="tip">only support CSV format file</div>
                </el-upload>
        </el-dialog>

        <el-dialog
              title="Recipe management"
              :visible.sync="RecipeManagementDialogVisible"
                style="text-align: left"
              >
            <u-table
              :data="dbRecipeList"
              :border="false"
              style="width: 100%">
              <template slot="empty">
                    no recipe currently
               </template>
              <u-table-column
                prop="name"
                label="name"
                width="360">
              </u-table-column>
              <u-table-column
                prop="operation"
                label="operation">
                <template v-slot="scope">
                    <el-button type="success" size="mini" @click="handleReuse(scope.row.value)">Reuse</el-button>
                    <el-button type="danger" size="mini" @click="handleRemove(scope.row.name)">Remove</el-button>
                </template>
              </u-table-column>
            </u-table>
        </el-dialog>
    </div>
</template>
<script>
  module.exports = {
    props: ['recipe_list', 'recipe_guidance_list', 'preview_dataset', 'split_column_indicator'],
    devServer: {
        proxy: 'http://127.0.0.1:5000/'
    },
    methods: {
        async preview() {
            this.$emit('is-loading-event', true);
            let submitRecipeList = this.getRecipe();
            this.$http.post('/preview', {
                    recipe_list: submitRecipeList
                }).then(response => {
                    if (response.body.code == 500) {
                        this.$message.error(response.body.message);
                    } else {
                        this.$emit('preview-dataset-changed', response.body);
                    }
                    this.$emit('is-loading-event', false);
                })

        },
        profiling(e) {
            e.preventDefault();
            this.domainKnowledgeDialogVisible = true;
        },
        handleConfirmClick() {
            if (this.domainKnowledge.needGuidance == "Yes") {
                this.$http.post('/domain_knowledge_capture', {domain_knowledge: this.domainKnowledge}).then(response => {
                    this.$emit('recipe-guidance-event', response.body)
                });
            }
            this.$emit('is-loading-event', true);
            this.has_profiled_prop = true;
            this.$http.post('/profiling', {}).then(response => {
                this.$emit('is-loading-event', false);
                this.$emit('profiling-event', response.body)
            });

            this.$http.get('/getdataset').then(response => {
               this.$emit('get-data-set-event', response.body)
            });
            this.domainKnowledgeDialogVisible = false
        },
        handleExport() {
            this.$emit('execute-export-event', true)
        },
        RecipeManagement() {
            this.$http.get('/recipe_list', ).then(response => {
                this.RecipeManagementDialogVisible = true;
                this.dbRecipeList = response.body;
            });
        },
        SaveRecipe() {
            this.$http.post('/store_recipe', {
                value: this.getRecipe()
            }).then(response => {
                this.$message.success('saving recipe successfully')
            });
        },
        getRecipe() {
            submitRecipeList = [];
            if (this.recipe_guidance_list.length > 0) {
                for (recipeGuidanceItem of this.recipe_guidance_list) {
                    if (recipeGuidanceItem.steps.length > 0) {
                        submitRecipeList = submitRecipeList.concat(recipeGuidanceItem.steps)
                    }
                }
            } else {
                submitRecipeList = this.recipe_list
            }
            return submitRecipeList;
        },
        handleReuse(recipeValue) {
            this.$emit('reuse-recipe-event', recipeValue);
            this.RecipeManagementDialogVisible = false;
            this.$message.success('Reusing recipe successfully');
        },
        handleRemove(name) {
            this.$http.post('/remove_recipe', {
                name: name
            }).then(response => {
                this.dbRecipeList = response.body;
            });
        },
        handleSplitColumnGuidance() {
            let submitRecipeList = this.getRecipe();
            this.$http.post('/split_guidance', {
                    recipe_list: submitRecipeList
                }).then(response => {
                    if (response.body.code == 500) {
                        this.$message.error(response.body.message);
                    } else {
                        this.$emit('split-guidance-response', response.body);
                    }
                    this.$emit('split-is-loading-event', false);
                })
        },
        uploadFile() {
            this.uploadDialogVisible = true
        }
    },
    data() {
      return {
        has_profiled_prop: false,
        domainKnowledgeDialogVisible: false,
        domainKnowledge: {
            needGuidance: "No",
            singleOrMultiple: "",
            needClean: "",
            needSplit: "",
            needAggregation: ""
        },
        recipeName: "",
        RecipeManagementDialogVisible: false,
        dbRecipeList: [],
        uploadDialogVisible: false
      }
    },
    watch: {
        split_column_indicator: function (oldVal, newVal) {
            this.handleSplitColumnGuidance();
        }
    }
  }
</script>
<style>
    .question_label {
        line-height: 40px; font-size: 14px; color: #606266; font-weight: bold
    }
</style>
Vue.use(VueBlobJsonCsv.default);
var vm = new window.Vue({
    el: '#inquery-modal',
    devServer: {
        proxy: 'http://127.0.0.1:5000/'
    },
    data: {
        is_loading: false,
        /*profiling result prop*/
        columnList: [],
        deleteColumns: [],
        fillMissingColumns: [],
        splitColumns: [],
        changeTypeColumns: [],
        /*submit props*/
        submitDeleteColumns: [],
        submitFillMissingColumns: [],
        submitSplitColumns: [],
        submitChangeTypeColumns: [],
        /*highlight props*/
        highlightColumnIndexes: [],
        highlightRowIndexes: [],
        highlightCellPositions: [],
        columnProfilingResult: {},
        /*preview props*/
        previewDataset: {},
        /*recipe list*/
        recipeList: [],
        recipeGuidanceList: [],
        /*refresh all the data among subcomponents*/
        refresh_key: 1,
        /*export*/
        export_key: 1
    },
    methods: {
        is_refresh() {
            console.log('start refresh compoent');
        },
        async submitForm(e) {
            e.preventDefault();
            const requestOptions = {
                method: "POST",
                headers: { 'Accept': 'application/json', "Content-Type": "application/json" },
                body: JSON.stringify({
                    removeColumns: this.removeColumns,
                    dateTime: this.dateTime,
                    dateTimeColumn: this.dateTimeColumn,
                    filename: this.filename
                })
            };
            const res = await fetch('http://127.0.0.1:5000/generateworkflow', requestOptions);
            result = await res.json();
        },
        handleHighlightColumnsChanged(message) {
            this.highlightColumnIndexes = message.index
        },
        handleColumnProfilingResult(message) {
            this.columnProfilingResult = message;
        },
        handlePreviewDatasetChanged(message) {
            this.previewDataset = message.preview_dataset;
            this.columnList = message.profiling_result.list_column_pre;
            this.deleteColumns = message.profiling_result.delete_column_pre;
            this.fillMissingColumns = message.profiling_result.fill_missing_value_pre;
            this.splitColumns = message.profiling_result.split_column_pre;
            this.changeTypeColumns = message.profiling_result.change_column_type_pre;
        },
        handleRecipeEvent(message) {
            //distribute this step into right guidance category
            if (this.recipeGuidanceList.length > 0) {
                for (recipeGuidanceItem of this.recipeGuidanceList) {
                    if (recipeGuidanceItem.type == message.guidance_category) {
                        recipeGuidanceItem.steps.push(message)
                    }
                }
            } else {
                this.recipeList.push(message);
            }
            this.$message.success('successfully add one step into recipe');
        },
        handleRemoveRecipeItemEvent(message) {
            this.recipeList.splice(message.item_index, 1);
            this.$message.warning('remove one step from recipe');
        },
        handleRemoveRecipeGuidanceEvent(message) {
            for (recipeGuidanceItem of this.recipeGuidanceList) {
                if (recipeGuidanceItem.type == message.guidance_category) {
                    recipeGuidanceItem.steps.splice(message.item_index, 1);
                }
            }
        },
        handleRecipeGuidanceEvent(message) {
            this.recipeGuidanceList = message
        },
        handleIsLoadingEvent(message) {
            this.is_loading = message
        },
        handleProfilingEvent(message) {
            this.columnList = message.list_column_pre;
            this.deleteColumns = message.delete_column_pre;
            this.fillMissingColumns = message.fill_missing_value_pre;
            this.splitColumns = message.split_column_pre;
            this.changeTypeColumns = message.change_column_type_pre;
        },
        handleGetDatasetEvent(message) {
            this.previewDataset = message
        },
        handleHasProfiledEvent(message) {
            this.hasProfiledProp = message;
        },
        handleExecuteExportEvent() {
            this.export_key += 1;
        },
        handleReuseRecipeEvent(message) {
            this.recipeList = this.recipeList.concat(message);
        }
    },
    components: {
        'display-table': window.httpVueLoader("/static/js/components/displayTable.vue"),
        'delete-column-group': window.httpVueLoader("/static/js/components/deleteColumnGroup.vue"),
        'column-status-panel': window.httpVueLoader("/static/js/components/columnStatus.vue"),
        'filling-missing-value-group': window.httpVueLoader("/static/js/components/fillingMissingValueGroup.vue"),
        'modal-footer': window.httpVueLoader("/static/js/components/footer.vue"),
        'recipe': window.httpVueLoader("/static/js/components/recipe.vue"),
        'profiling-column': window.httpVueLoader("/static/js/components/profilingColumn.vue"),
        'splitting-column-group': window.httpVueLoader("/static/js/components/splittingColumnGroup.vue"),
        'change-column-type-group': window.httpVueLoader("/static/js/components/changeColumnType.vue"),
        'query-builder-group': window.httpVueLoader("/static/js/components/queryBuilderGroup.vue"),
        'group-by': window.httpVueLoader("/static/js/components/groupby.vue"),
        'multiple-file-wrangling': window.httpVueLoader("/static/js/components/multipleFileWrangling.vue"),
        'chart': window.httpVueLoader("/static/js/components/chart.vue")

    },
    delimiters: ["${","}"]

});

vm.$on('refresh', function(id) {
        vm.$data.is_loading = false;
        /*profiling result prop*/
        vm.$data.columnList = [];
        vm.$data.deleteColumns = [];
        vm.$data.fillMissingColumns = [];
        vm.$data.splitColumns = [];
        vm.$data.changeTypeColumns = [];
        /*submit props*/
        vm.$data.submitDeleteColumns = [];
        vm.$data.submitFillMissingColumns = [];
        vm.$data.submitSplitColumns = [];
        vm.$data.submitChangeTypeColumns = [];
        /*highlight props*/
        vm.$data.highlightColumnIndexes = [];
        vm.$data.highlightRowIndexes = [];
        vm.$data.highlightCellPositions = [];
        vm.$data.columnProfilingResult = {};
        /*preview props*/
        vm.$data.previewDataset = {};
        /*recipe list*/
        vm.$data.recipeList = [];
        vm.$data.hasProfiledProp = false;
        vm.$data.refresh_key = Math.random();
});
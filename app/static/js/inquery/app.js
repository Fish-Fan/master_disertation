new window.Vue({
    el: '#inquery-modal',
    devServer: {
        proxy: 'http://127.0.0.1:5000/'
    },
    data: {
        is_loading: false,
        /*profiling result prop*/
        columnList: {},
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
        recipeList: []
    },
    methods: {
        profiling(e) {
            e.preventDefault();
            this.is_loading = true;
            this.$http.post('/profiling', {}).then(response => {
                result = response.body;
                this.columnList = result.list_column_pre;
                this.deleteColumns = result.delete_column_pre;
                this.fillMissingColumns = result.fill_missing_value_pre;
                this.splitColumns = result.split_column_pre;
                this.changeTypeColumns = result.change_column_type_pre;
                this.is_loading = false;
            });

            this.$http.get('/getdataset').then(response => {
               this.previewDataset = response.body;
            })
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
            this.recipeList.push(message);
        },
        handleRemoveRecipeItemEvent(message) {
            this.recipeList.splice(message.item_index, 1);
        },
        handleIsLoadingEvent(message) {
            this.is_loading = message
        }

    },
    components: {
        'display-table': window.httpVueLoader("/static/js/components/displayTable.vue"),
        'delete-column-group': window.httpVueLoader("/static/js/components/deleteColumnGroup.vue"),
        'column-status-panel': window.httpVueLoader("/static/js/components/columnStatus.vue"),
        'filling-missing-value-group': window.httpVueLoader("/static/js/components/fillingMissingValueGroup.vue"),
        'preview-and-add-recipe-group': window.httpVueLoader("/static/js/components/previewAndAddRecipeGroup.vue"),
        'recipe': window.httpVueLoader("/static/js/components/recipe.vue"),
        'profiling-column': window.httpVueLoader("/static/js/components/profilingColumn.vue"),
        'splitting-column-group': window.httpVueLoader("/static/js/components/splittingColumnGroup.vue"),
        'change-column-type-group': window.httpVueLoader("/static/js/components/changeColumnType.vue"),
        'stringRule': window.httpVueLoader("/static/js/components/stringRule.vue"),
        'query-builder-group': window.httpVueLoader("/static/js/components/queryBuilderGroup.vue"),
        'group-by': window.httpVueLoader("/static/js/components/groupby.vue"),
        'multiple-file-wrangling': window.httpVueLoader("/static/js/components/multipleFileWrangling.vue")

    },
    delimiters: ["${","}"]

})
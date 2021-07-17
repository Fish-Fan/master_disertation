new window.Vue({
    el: '#inquery-modal',
    data: {
        filename: 'new_uk_500.csv',
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
        previewDeleteColumns: [],
        previewFillMissingColumns: [],
        previewSplittingColumns: [],
        previewChangeTypeColumns: [],
        previewDataset: {},
        /*recipe list*/
        recipeList: []
    },
    methods: {
        async profiling(e) {
            e.preventDefault();
            const requestOptions = {
                method: "POST",
                headers: { 'Accept': 'application/json', "Content-Type": "application/json" },
                body: JSON.stringify({ filename: this.filename })
            };
            const res = await fetch('http://127.0.0.1:5000/profiling', requestOptions);
            result = await res.json();
            this.columnList = result.list_column_pre;
            this.deleteColumns = result.delete_column_pre;
            this.fillMissingColumns = result.fill_missing_value_pre;
            this.splitColumns = result.split_column_pre;
            this.changeTypeColumns = result.change_column_type_pre;
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
        demoFun (message, e) {
            e.preventDefault()
            console.log(message)
        },
        handleHighlightColumnsChanged(message) {
            this.highlightColumnIndexes = message.index
        },
        handleColumnProfilingResult(message) {
            this.columnProfilingResult = message;
        },
        handlePreviewDatasetChanged(message) {
            this.previewDataset = message;
            var column_list_new = [];
            for (item of message.headers) {
                column_list_new.push({index: item.index, type: item.type, name: item.prop});
            }
            this.columnList = column_list_new;
        },
        handleRecipeEvent(message) {
            switch (message.type) {
              case 'deleteColumn':
                this.previewDeleteColumns = message.data;
                this.recipeList.push(message);
                break;
              case 'fillMissingValue':
                this.previewFillMissingColumns.push(message.data);
                this.recipeList.push(message);
                break;
              case 'splittingColumnValue':
                this.previewSplittingColumns.push(message.data);
                this.recipeList.push(message);
                break;
              case 'changeColumnType':
                this.previewChangeTypeColumns.push(message.data);
                this.recipeList.push(message);
                break;
              default:
                console.log(`Sorry, we are out of ${expr}.`);
            }
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

    },
    delimiters: ["${","}"]

})
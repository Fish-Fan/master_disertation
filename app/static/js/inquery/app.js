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
            this.changeTypeColumns = result.change_column_pre;
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
            tagObj = {
                'distinct_count_without_nan': {
                    'value': message.distinct_count_without_nan
                },
                'is_unique': {
                    'value': message.is_unique,
                    'type': 'success'
                },
                'p_missing': {
                    'value': this.roundUtil(message.p_missing) * 100 + '%',
                    'type': 'danger'
                },
                'p_distinct': {
                    'value': this.roundUtil(message.p_distinct) * 100 + '%',
                    'type': 'info'
                },
                'top-frequency': {
                    'value': message.top,
                    'type': 'warning'
                }
            }
            this.columnProfilingResult = tagObj
        },
        handlePreviewDatasetChanged(message) {
            this.previewDataset = message
        },
        roundUtil(num) {
            return Math.round(num * 10000) / 10000
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
              case 'Papayas':
                console.log('Mangoes and papayas are $2.79 a pound.');
                // expected output: "Mangoes and papayas are $2.79 a pound."
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
        'profiling-column': window.httpVueLoader("/static/js/components/profilingColumn.vue")
    },
    delimiters: ["${","}"]

})
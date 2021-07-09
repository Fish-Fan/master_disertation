new window.Vue({
    el: '#inquery-modal',
    data: {
        filename: 'new_uk_500.csv',
        deleteColumns: [],
        fillMissingColumns: [],
        splitColumns: [],
        changeTypeColumns: [],
        submitDeleteColumns: [],
        submitFillMissingColumns: [],
        submitSplitColumns: [],
        submitChangeTypeColumns: []
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
        }
    },
    components: {
        'display-table': window.httpVueLoader("/static/js/components/displayTable.vue"),
        'checkbox-btn-group': window.httpVueLoader("/static/js/components/checkboxButton.vue")
    },
    delimiters: ["${","}"]

})
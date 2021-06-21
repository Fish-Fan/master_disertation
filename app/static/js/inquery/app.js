const app = Vue.createApp({
    data () {
        return {
            columns: [],
            constantColumns: [],
            highCorrelationColumns: [],
            manyZerosColumns: [],
            blankColumns: [],
            reportPath: '/static/report_html/demo.html',
            removeColumns: [],
            dateTime: [],
            dateTimeColumn: '',
            filename: 'qqq.csv'
        }
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
            this.columns = result.columns;
            this.constantColumns = result.constant;
            this.highCorrelationColumns = result.correlation;
            this.manyZerosColumns = result.zero;
            this.blankColumns = result.missing;
            this.reportPath = '/static/report_html/' + result.reportName;
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
        }
    },
    compilerOptions: {
     delimiters: ['${', '}'],
        comments: true
    }
});

app.mount('#inquery-modal');
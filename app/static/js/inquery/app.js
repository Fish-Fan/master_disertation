const app = Vue.createApp({
    data () {
        return {
            columns: [],
            constantColumns: [],
            highCorrelationColumns: [],
            manyZerosColumns: [],
            blankColumns: []
        }
    },
    methods: {
        async profiling() {
            const requestOptions = {
                method: "POST",
                headers: { 'Accept': 'application/json', "Content-Type": "application/json" },
                body: JSON.stringify({ filename: "qqq.csv" })
            };
            const res = await fetch('http://127.0.0.1:5000/profiling', requestOptions);
            result = await res.json();
            this.columns = ["Sdate", "Cosit", "LaneNumber", "LaneDescription", "LaneDirection", "DirectionDescription", "Volume", "Flags", "Flag Text", "AvgSpeed", "PmlHGV", "Class1Volume", "Class2Volume", "Class3Volume", "Class4Volume", "Class5Volume", "Class6Volume"];
            this.constantColumns = result.constant;
            this.highCorrelationColumns = result.correlation;
            this.manyZerosColumns = result.zero;
            this.blankColumns = result.missing;
        }
    },
    compilerOptions: {
     delimiters: ['${', '}'],
        comments: true
    }
});

app.mount('#inquery-modal');
<template>
  <el-tabs value="View">
    <el-tab-pane label="Data Preview" name="View" style="margin-bottom: 20px">
        <canvas id="myChart" width="400" height="400"></canvas>
    </el-tab-pane>
  </el-tabs>


</template>


<script>
    module.exports = {
        mounted() {
            var ctx = document.getElementById('myChart').getContext('2d');
            var myChart = new Chart(ctx, {
                type: 'bar',
                data: this.chartData,
                options: this.chartOption
            })
        },
        props: ['highlight_columns', 'preview_dataset', 'is_loading'],
        devServer: {
            proxy: 'http://127.0.0.1:5000/'
        },
        methods: {

        },
        watch: {

        },
        data() {
            return {
                chartData: {
                    labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
                    datasets: [{
                        label: '# of Votes',
                        data: [12, 19, 3, 5, 2, 3],
                        backgroundColor: [
                            'rgba(255, 99, 132, 0.2)',
                            'rgba(54, 162, 235, 0.2)',
                            'rgba(255, 206, 86, 0.2)',
                            'rgba(75, 192, 192, 0.2)',
                            'rgba(153, 102, 255, 0.2)',
                            'rgba(255, 159, 64, 0.2)'
                        ],
                        borderColor: [
                            'rgba(255, 99, 132, 1)',
                            'rgba(54, 162, 235, 1)',
                            'rgba(255, 206, 86, 1)',
                            'rgba(75, 192, 192, 1)',
                            'rgba(153, 102, 255, 1)',
                            'rgba(255, 159, 64, 1)'
                        ],
                        borderWidth: 1
                    }]
                },
                chartOption: {
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            }
        }
    }
</script>
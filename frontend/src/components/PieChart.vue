<template>
    <div id="chart-pie">
        <apexchart type="pie" :options="chartOptions" :series="series" class="chart">
        </apexchart>
    </div>
</template>

<script>
export default {

    props: {
        chartPieData: {
            type: Object,
            required: true,
        }
    },

    name: 'PieChart',
    data() {
        return {
            series: [],
            chartOptions: {
                labels: [
                    "ОРЛОВСКАЯ ОБЛАСТЬ"
                ],
            },
        };
    },

    watch: {
        chartPieData: {
            handler(newValue, oldValue) {
                this.updatePieChart(newValue);
            },
            deep: true,
        },
    },

    methods: {
        async updatePieChart(chartData) {
            if (chartData) {
                this.chartOptions.labels = await chartData.categories;
                this.series = await chartData.series;
            };
        },
    },
};

</script>

<style scoped>
.chart-pie {
    width: 100%;
    font-weight: auto;
}
</style>

<template>
    <div class="chart-line">
        <apexchart ref="chart" type="line" :options="chartOptions" :series="series" class="chart"></apexchart>
    </div>
</template>

<script>
export default {
    props: {
        chartLineData: {
            type: Object,
            required: true,
        }
    },
    name: 'LineChart',
    data() {
        return {
            chartOptions: {
                chart: {
                    id: 'vuechart-line',
                    toolbar: { show: true },
                },
                xaxis: {
                    categories: [
                        "2025-02-05",
                        "2025-02-06",
                        "2025-02-07",
                        "2025-02-08",
                        "2025-02-09",
                        "2025-02-10",
                        "2025-02-11"
                    ],
                    labels: {
                        style: {
                            colors: ['#FFFFFF'],
                            fontSize: '14px',
                            fontWeight: 'bold',
                        },
                    },
                },
                yaxis: {
                    labels: {
                        style: {
                            colors: ['#FFFFFF'],
                            fontSize: '14px',
                            fontWeight: 'bold',
                        },
                    },
                },
                title: {
                    text: 'График опубликованных НПА',
                    align: 'center',
                    style: {
                        fontSize: '24px',
                        color: '#FFFFFF',
                        fontWeight: 'bold',
                    },
                },
                legend: {
                    labels: {
                        colors: ['#FFFFFF'],
                    },
                },
                colors: ['#A8D8B9', '#F1C6B5', '#B2A3D3'],
                tooltip: {
                    theme: 'dark',
                    style: {
                        fontSize: '14px',
                        color: '#FFFFFF',
                        background: '#2C3E50',
                    },
                },
                grid: { borderColor: '#2C3E50' },
                stroke: {
                    curve: 'smooth',
                    width: 1.5,
                },
                dataLabels: {
                    enabled: true,
                    style: {
                        colors: ['#FFFFFF'],
                        fontSize: '12px',
                        fontWeight: 'bold',
                    },
                },
            },
            series: [],
        };
    },


    watch: {
        chartLineData: {
            handler(newValue, oldValue) {
                this.updateLineChart(newValue);
            },
            deep: true,
        },
    },

    methods: {
        async updateLineChart(chartData) {
            if (chartData) {
                this.series = await chartData.series;
                this.chartOptions.xaxis.categories = await chartData.categories;
                /* for (let i = 0; i < 7; i++) {
                    this.chartOptions.xaxis.categories.push(Date());
                }; */
                /* this.computeData(); */
            };
        },
    },

};
</script>

<style scoped>
.chart-line {
    width: 100%;
    font-weight: auto;
}
</style>

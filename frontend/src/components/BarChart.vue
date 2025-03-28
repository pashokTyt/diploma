<!-- пока все со статическими данными -->
<template>
    <div class="chart-bar">
        <apexchart type="bar" :options="chartOptions" :series="series" class="chart">
        </apexchart>
    </div>
</template>

<script>
export default {
    props: {
        chartBarData: {
            type: Object,
            required: true,
        }
    },

    name: 'BarChart',

    data() {
        return {
            chartOptions: {
                chart: {
                    id: 'vuechart-bar',
                    toolbar: { show: true },
                },
                xaxis: {
                    categories: [
                        "min-just",
                        "orel-region",
                        "pravo.gov.ru"
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
                        colors: '#FFFFFF',
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
                plotOptions: {
                    bar: {
                        horizontal: false,
                        columnWidth: '55%',
                        endingShape: 'rounded',
                    },
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
        chartBarData: {
            handler(newValue, oldValue) {
                this.updateBarChart(newValue);
            },
            deep: true,
        },
    },

    methods: {
        async updateBarChart(chartData) {
            if (chartData) {
                this.chartOptions.xaxis.categories = await chartData.categories;
                this.series = await chartData.series;
            };
        },
    },
};
</script>


<style scoped>
.chart-bar {
    width: 100%;
    font-weight: auto;
}
</style>
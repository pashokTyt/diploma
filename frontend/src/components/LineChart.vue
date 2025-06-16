<template>
    <div class="chart-line">
        <apexchart ref="chart" type="line" :options="chartOptions" :series="series" class="chart"></apexchart>
    </div>
</template>

<script>
export default {
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
                    width: 4,
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
    created() {
        this.series = this.generateRandomSeries(3, 7, 5, 30);
    },
    methods: {
        // Генерация массива случайных чисел длиной count в диапазоне [min, max]
        generateRandomData(count, min, max) {
            const data = [];
            for (let i = 0; i < count; i++) {
                data.push(Math.floor(Math.random() * (max - min + 1)) + min);
            }
            return data;
        },
        // Генерация массива серий с уникальными именами и случайными данными
        generateRandomSeries(seriesCount, pointsCount, minValue, maxValue) {
            const series = [];
            for (let i = 1; i <= seriesCount; i++) {
                series.push({
                    name: `Серия ${i}`,
                    data: this.generateRandomData(pointsCount, minValue, maxValue),
                });
            }
            return series;
        }
    }
};
</script>

<style scoped>
.chart-line {
    width: 100%;
    font-weight: auto;
}
</style>

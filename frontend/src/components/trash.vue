<template>
  <div class="dashboard">
    <main>
      <div class="row">
        <div class="col-md-3">
          <section class="stats">
            <h2>За сутки:</h2>
            <div class="stat">
              <h2>Опубликованные НПА</h2>
              <p>{{ publishedNpasCount }}</p>
            </div>
            <div class="stat">
              <h2>Неопубликованные НПА</h2>
              <p>{{ unpublishedNpasCount }}</p>
            </div>
            <div class="stat">
              <h2>Регионы</h2>
              <p>{{ regionsCount }}</p>
            </div>
            <div class="stat">
              <h2>Источники</h2>
              <p>{{ sourcesCount }}</p>
            </div>
            <div class="stat">
              <h2>Просроченных</h2>
              <p>{{ overdueCount }}</p>
            </div>
            <div class="select-region">
              <el-cascader
                v-model="selectedRegion"
                :options="formattedRegions"
                :props="cascaderProps"
                clearable
                multiple
                filterable
                allow-create
                default-first-option
                :reserve-keyword="false"
                size="large"
                placeholder="Выбраны все субъекты РФ"
                style="width: 100%"
              />
            </div>
          </section>

          
        </div>

        <div class="col-md-9">
          <section class="charts">
            <div id="monitoring-widget">
              <h2 class="text-xl font-bold mb-2">Мониторинг опубликования:</h2>
              <LineChart v-bind="{ chartLineData: chartLineData }" />
            </div>
          </section>
        </div>
      </div>

      <div class="row">
        <div class="col-md-6">
          <section class="charts">
            <div id="subjects-widget">
              <h2 class="text-xl font-bold mb-2">Субъекты РФ:</h2>
              <PieChart v-bind="{ chartPieData: chartPieData }" />
            </div>
          </section>
        </div>
        <div class="col-md-6">
          <section class="charts">
            <h2>Распределение по источникам</h2>
            <div id="sources-widget">
              <BarChart v-bind="{ chartBarData: chartBarData }" />
            </div>
          </section>
        </div>
        <div class="latest-npa">
            <h4>Последние опубликованные НПА:</h4>
            <div class="npa-list">
              <div v-for="(npa, index) in latestNpas" :key="index" class="npa-item">
                {{ npa }}
              </div>
            </div>
          </div>
      </div>
    </main>
  </div>
</template>

<script>
import LineChart from './LineChart.vue';
import BarChart from './BarChart.vue';
import PieChart from './PieChart.vue';
import { selectedRegion } from '@/pinia';
import { useRegionsStore } from '@/pinia';

export default {
  components: {
    LineChart,
    BarChart,
    PieChart,
  },
  data() {
    return {
      publishedNpasCount: 0,
      unpublishedNpasCount: 0,
      regionsCount: 0,
      sourcesCount: 0,
      overdueCount: 0,
      chartLineData: {},
      chartBarData: {},
      chartPieData: {},
      selectedRegion: null,
      latestNpas: [],
      loading: true,
      error: null,
      cascaderProps: {
        value: 'value',
        label: 'label',
        children: 'children',
      },
    };
  },
  async created() {
    const regionsStore = useRegionsStore();
    try {
      await regionsStore.fetchRegions();
    } catch (err) {
      this.error = 'Ошибка при загрузке данных регионов';
      console.error(err);
    }
  },
  async mounted() {
    await this.loadDashboardData();
    await this.updateChartData();
  },
  methods: {
    getSelectedRegion() {
      const store = selectedRegion();
      const regionName = store.getRegionName;
      const regionNameAsString = regionName ? regionName.toString() : null;
      this.selectedRegion = regionNameAsString;
      return regionNameAsString;
    },
    async loadDashboardData() {
      try {
        this.loading = true;
        const response = await this.$http.get('/api/dashboard/');
        const data = response.data;
        this.publishedNpasCount = data.publishedNpasCount;
        this.unpublishedNpasCount = data.unpublishedNpasCount;
        this.regionsCount = data.regionsCount;
        this.sourcesCount = data.sourcesCount;
        this.overdueCount = data.overdueCount;
        this.latestNpas = data.latestNpas;
      } catch (error) {
        this.error = 'Ошибка при загрузке статистики дашборда';
        console.error(error);
      } finally {
        this.loading = false;
      }
    },
    async updateChartData() {
      const regionNameString = this.getSelectedRegion();
      try {
        const response = await this.$http.get('api/published-npa/get_chart_data/', {
          params: {
            region_name: regionNameString,
          },
        });
        this.chartLineData = response.data.count_all_per_day || {};
        this.chartBarData = response.data.count_sources || {};
        this.chartPieData = response.data.count_regions || {};
      } catch (error) {
        console.error('Ошибка при получении данных графиков:', error);
      }
    },
    async handleRegionSelected(regionName) {
      console.log('Выбран регион в родительском компоненте:', regionName);
      this.selectedRegion = regionName;
      await this.updateChartData();
    },
  },
  computed: {
    formattedRegions() {
      const regionsStore = useRegionsStore();
      return regionsStore.getRegions.map((region) => ({
        value: region.code,
        label: region.label,
      }));
    },
  },
};
</script>

<style scoped>
.dashboard {
  max-width: 1800px;
  margin: 0 auto;
  padding: 20px;
  background-color: #f9f9f9;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

header {
  background-color: #2c3e50;
  color: white;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 30px;
}

main {
  padding: 20px;
}

.stats {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.stat {
  margin-bottom: 20px;
}

.stat h2 {
  font-size: 1.1rem;
  color: #666;
  margin-bottom: 5px;
}

.stat p {
  font-size: 1.8rem;
  font-weight: 500;
  color: #2c3e50;
}

.select-region select {
  width: 100%;
  padding: 10px;
  border-radius: 4px;
  border: 1px solid #ddd;
  background: white;
}

.charts {
  background: white;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 30px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  width: 100%;
}

.chart-container {
  margin-top: 20px;
}

.npa-list,
.news-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.npa-item,
.news-item {
  padding: 12px 0;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
}

.npa-date,
.news-date {
  color: #666;
  min-width: 120px;
}

.npa-name,
.news-title {
  flex-grow: 1;
  margin-left: 20px;
}

.chart-placeholder img {
  width: 100%;
  border-radius: 4px;
  opacity: 0.7;
}

@media (max-width: 768px) {
  .stat p {
    font-size: 1.4rem;
  }

  .npa-item,
  .news-item {
    flex-direction: column;
  }

  .npa-date,
  .news-date {
    margin-bottom: 5px;
  }
}

.latest-npa {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-top: 5%;
  margin-bottom: 5%;
}
</style>

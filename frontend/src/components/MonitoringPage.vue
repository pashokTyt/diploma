<template>
  <!-- map -->
  <div id="map-widget">
    <h2 class="text-xl font-bold mb-2">Карта регионов:</h2>
    <!--     <el-button round @click="updateChartData()">Обновить графики</el-button>
    <p></p> -->
    <div class="map-component">
      <MapComponent @region-selected="handleRegionSelected" />
    </div>
  </div>


<!--     <div class="col-sm">
      <div id="monitoring-widget">
        <h2 class="text-xl font-bold mb-2">Мониторинг опубликования:</h2>
        <LineChart v-bind="{ chartLineData: chartLineData }" />
      </div>
    </div> -->

<!--     <div class="col-sm">
      <div id="sources-widget">
        <h2 class="text-xl font-bold mb-2">Источники опубликования за сутки:</h2>
        <BarChart v-bind="{ chartBarData: chartBarData }" />
      </div>
    </div> -->

<!--     <div class="col-sm">
      <div id="subjects-widget">
        <h2 class="text-xl font-bold mb-2">Субъекты РФ:</h2>
        <PieChart v-bind="{ chartPieData: chartPieData }" />
      </div>
    </div> -->

</template>

<script>
import MapComponent from './MapComponent.vue';
import LineChart from './LineChart.vue';
import BarChart from './BarChart.vue';
import PieChart from './PieChart.vue';
import { selectedRegion } from '@/pinia';

export default {
  components: {
    MapComponent,
    LineChart,
    BarChart,
    PieChart,
  },
  data() {
    return {
      chartLineData: [],
      chartBarData: [],
      chartPieData: [],
      selectedRegion: null,
    }
  },
  async mounted() {
    await this.updateChartData();
  },

  methods: {
    getSelectedRegion() {
      const store = selectedRegion();
      const regionName = store.getRegionName;
      const regionNameAsString = regionName.toString();
      this.selectedRegion = regionNameAsString;
      return regionNameAsString;
    },

    async updateChartData() {
      const regionNameString = this.getSelectedRegion();
      try {
        const response = await this.$http.get(`api/published-npa/get_chart_data/`, {
          params: {
            region_name: regionNameString,
          },
        });
        this.chartLineData = response.data.count_all_per_day;
        this.chartBarData = response.data.count_sources;
        this.chartPieData = response.data.count_regions;
      } catch (error) {
        console.error('Ошибка при получении данных:', error);
      }
    },

    async handleRegionSelected(regionName) {
      console.log("Выбран регион в родительском компоненте:", regionName);
      this.selectedRegion = regionName;
      await this.updateChartData();
    },
  },
};
</script>

<style scoped>

</style>

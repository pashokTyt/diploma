<template>
  <p></p>
  <div class="container-fluid">
    <div class="row">
      <!-- filter(published, date, source, region) -->
      <div class="col-md-2">
        <h2>Фильтры</h2>
        <div class="filter-panel">
          <div class="filter-elements">
            <div class="row">
              <el-checkbox v-model="checked" label="Опубликованы" size="large" @change="fetchNpas" border />
            </div>
            <p></p>
            <div class="row">
              <span>Дата публикации:</span>
              <el-date-picker v-model="selectedWriteDateRange" type="daterange" range-separator="По"
                start-placeholder="Начало" end-placeholder="Конец" :size="'small'" @change="fetchNpas"
                format="DD.MM.YYYY" unlink-panels />
            </div>
            <p></p>
            <div class="row">
              <label for="source">Источник:</label>
              <el-cascader v-model="selectedSource" :options="formattedSources" :props="cascaderProps" clearable
                @change="fetchNpas" />
            </div>
            <p></p>
            <div class="row">
              <label for="region">Регион:</label>
              <el-cascader v-model="selectedRegion" :options="formattedRegions" :props="cascaderProps" clearable
                @change="fetchNpas" />
            </div>
          </div>
        </div>
      </div>
      <!-- search, table, pagination -->
      <div class="col-md-9">
        <h2>Список неопубликованных НПА</h2>
        <div class="search-table-pagination">
          <!-- search -->
          <form @submit.prevent="submitForm" class="form-inline my-2 my-lg-0 d-flex align-items-center">
            <input class="form-control mr-4" type="search" placeholder="Поиск по названию" aria-label="Найти"
              v-model.trim="query" style="flex: 1;" @input="applyFilters">
          </form>
          <!-- table -->
          <table-element :paginated_npas="filteredNpas" v-loading="loading" />
          <!-- pagination -->
          <div class="demo-pagination-block">
            <el-pagination :current-page="currentPage" :page-size="itemsPerPage" :page-sizes="[10, 50, 100, 150]"
              layout="total, sizes, prev, pager, next, jumper" :total="totalNpas" @size-change="handleSizeChange"
              @current-change="handleCurrentChange" />
          </div>
        </div>
      </div>

    </div>
  </div>

</template>

<script>
import TableElement from './TableElement.vue';
import { useSourcesStore } from '@/pinia';
import { useRegionsStore } from '@/pinia';

export default {
  components: {
    TableElement,
  },
  data() {
    return {
      query: '',
      selectedSource: [],
      selectedRegion: null,
      selectedWriteDateRange: [],
      currentPage: 1,
      itemsPerPage: 10,
      totalNpas: 0,
      cascaderProps: {
        value: 'value',
        label: 'label',
        children: 'children'
      },
      filteredNpas: [],
      checked: false,
      error: null,
      loading: true,
    };
  },


  async created() {
    const sourcesStore = useSourcesStore();
    const regionsStore = useRegionsStore();
    try {
      await sourcesStore.fetchSources();
      await regionsStore.fetchRegions();
      await this.fetchNpas();
    } catch (err) {
      this.error = 'Ошибка при загрузке данных';
    }
  },

  computed: {
    //костыли
    formattedSources() {
      const sourcesStore = useSourcesStore();
      const sources = sourcesStore.getSources.map(source => ({
        value: source.label,
        label: source.label,
        url_address: source.url_address,
      }));
      return sources;
    },

    formattedRegions() {
      const regionsStore = useRegionsStore();
      return regionsStore.getRegions.map(region => ({
        value: region.code,
        label: region.label,
      }));
    },
  },

  methods: {
    submitForm() {
      this.fetchNpas();
    },
    // основная функция, запрос -> получение НПА
    async fetchNpas() {
      try {
        this.loading = true
        const response = await this.$http.get(`api/published-npa/`, {
          params: {
            region_code: Array.isArray(this.selectedRegion) ? this.selectedRegion[0] : this.selectedRegion,
            source_name: Array.isArray(this.selectedSource) && this.selectedSource.length > 0 ? this.selectedSource[0] : undefined,
            publish_date_after: this.selectedWriteDateRange[0] ? this.selectedWriteDateRange[0].toISOString().split('T')[0] : undefined,
            publish_date_before: this.selectedWriteDateRange[1] ? this.selectedWriteDateRange[1].toISOString().split('T')[0] : undefined,
            published: this.checked,
            search: this.query,
            page: this.currentPage,
            size: this.itemsPerPage,
          },
        });
        this.filteredNpas = response.data.results || []; // Список НПА
        this.totalNpas = response.data.count || 0; // Общее количество записей
        this.loading = false;

      } catch (error) {
      }
    },

    applyFilters() {
      this.currentPage = 1;
      return this.fetchNpas();
    },

    handleSizeChange(newSize) {
      this.itemsPerPage = newSize;
      this.fetchNpas();
    },

    handleCurrentChange(newPage) {
      if (newPage > Math.ceil(this.totalNpas / this.itemsPerPage)) {
        console.log("Выбрать другую старницу")
        return;
      }

      this.currentPage = newPage;
      this.fetchNpas();
    },
  },
};
</script>

<style>
.demo-pagination-block {
  margin: 1%;
  display: flex;
  justify-content: center;
  margin-bottom: 1%;
}
</style>

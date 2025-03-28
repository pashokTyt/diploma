<template>
  <div class="table-container">
    <div class="scrollable-table">
      <el-table :data="paginated_npas" style="width: 100%">
        <el-table-column prop="name" label="Название" min-width="500"></el-table-column>
        <el-table-column prop="number" label="Номер" min-width="70"></el-table-column>
        <el-table-column prop="publish_date" label="Опубликован" sortable min-width="113"></el-table-column>
        <el-table-column prop="write_date" label="Подписан" sortable min-width="110"></el-table-column>
        <el-table-column prop="source.name" label="Источник" min-width="150"></el-table-column>
        <el-table-column prop="region.name" label="Регион" min-width="200"></el-table-column>
        <el-table-column label="Ссылка на скачивание" min-width="150">
          <template #default="{ row }">
            <a :href="row.link_to_download" class="download-link">Скачать</a>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    paginated_npas: {
      type: Array,
      required: true,
    }
  }
};
</script>

<style scoped>
.table-container {
  width: 100%;
  margin-top: 1%;
}

.scrollable-table {
  max-height: 600px;
  overflow-y: auto;
}

</style>
